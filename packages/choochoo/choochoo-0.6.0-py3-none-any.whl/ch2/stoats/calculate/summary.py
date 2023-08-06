
from random import choice
from re import split

from . import IntervalCalculator
from ...lib.date import local_date_to_time, time_to_local_date
from ...lib.schedule import Schedule
from ...squeal.database import add
from ...squeal.tables.source import Interval
from ...squeal.tables.statistic import StatisticJournal, StatisticName, StatisticMeasure, STATISTIC_JOURNAL_CLASSES, \
    StatisticJournalType


class SummaryStatistics(IntervalCalculator):

    def run(self, force=False, after=None, schedule=None):
        if not schedule:
            raise Exception('schedule=... karg required')
        schedule = Schedule(schedule)
        super().run(force=force, after=after, schedule=schedule)

    def _filter_intervals(self, q, schedule=None):
        return q.filter(Interval.schedule == schedule,
                        Interval.owner == self)

    def _statistics_missing_summaries(self, s, start, finish):
        statistics_with_data_but_no_summary = s.query(StatisticName.id). \
            join(StatisticJournal). \
            filter(StatisticJournal.time >= start,
                   StatisticJournal.time < finish,
                   StatisticName.summary != None)
        # avoid duplicates
        return s.query(StatisticName). \
            filter(StatisticName.id.in_(statistics_with_data_but_no_summary)). \
            all()

    def _journal_data(self, s, statistic_name, start, finish):
        return s.query(StatisticJournal). \
            filter(StatisticJournal.statistic_name == statistic_name,
                   StatisticJournal.time >= start,
                   StatisticJournal.time < finish).all()

    def _calculate_value(self, summary, values, schedule, input):
        range = schedule.describe()
        type, units = input.type, input.statistic_name.units
        defined = [x for x in values if x is not None]
        if summary == 'min':
            return min(defined) if defined else None, 'Min/%s %%s' % range, type, units
        elif summary == 'max':
            return max(defined) if defined else None, 'Max/%s %%s' % range, type, units
        elif summary == 'sum':
            return sum(defined, 0), 'Total/%s %%s' % range, type, units
        elif summary == 'avg':
            return (sum(defined) / len(defined) if defined else None, 'Avg/%s %%s' % range,
                    StatisticJournalType.FLOAT, units)
        elif summary == 'med':
            defined = sorted(defined)
            if len(defined):
                if len(defined) % 2:
                    return defined[len(defined) // 2], 'Med/%s %%s' % range, StatisticJournalType.FLOAT, units
                else:
                    return 0.5 * (defined[len(defined) // 2 - 1] + defined[len(defined) // 2]), \
                           'Med/%s %%s' % range, StatisticJournalType.FLOAT, units
            else:
                return None, 'Med/%s %%s' % range, StatisticJournalType.FLOAT, units
        elif summary == 'cnt':
            if type == StatisticJournalType.TEXT:
                n = len([x for x in defined if x.strip()])
            else:
                n = len(defined)
            return n, 'Cnt/%s %%s' % range, StatisticJournalType.INTEGER, 'entries'
        elif summary == 'msr':  # measure handled separately
            return None, None, None, None
        else:
            self._log.warn('No algorithm for "%s"' % summary)
            return None, None, None, None

    def _get_statistic_name(self, s, root, name, units):
        # we use the old statistic id as the constraint.  this lets us handle multiple
        # statistics with the same name, but different owners and constraints.
        statistic_name = s.query(StatisticName). \
            filter(StatisticName.name == name,
                   StatisticName.owner == self,
                   StatisticName.constraint == root).one_or_none()
        if not statistic_name:
            statistic_name = add(s, StatisticName(name=name, owner=self, constraint=root, units=units))
        if statistic_name.units != units:
            self._log.warn('Changing units on %s (%s -> %s)' % (statistic_name.name, statistic_name.units, units))
            statistic_name.units = units
        return statistic_name

    def _create_value(self, s, interval, spec, statistic_name, summary, data, values, time):
        value, template, type, units = self._calculate_value(summary, values, spec, data[0])
        if value is not None:
            name = template % statistic_name.name
            new_name = self._get_statistic_name(s, statistic_name, name, units)
            journal = add(s, STATISTIC_JOURNAL_CLASSES[type](
                statistic_name=new_name, source=interval, value=value, time=time))
            self._log.debug('Created %s over %s for %s' % (journal, interval, statistic_name))

    def _create_measures(self, s, interval, spec, statistic, data):
        # we only rank non-NULL values
        ordered = sorted([journal for journal in data if journal.value is not None],
                         key=lambda journal: journal.value, reverse=True)
        n, measures = len(ordered), []
        for rank, journal in enumerate(ordered, start=1):
            if n > 1:
                percentile = (n - rank) / (n - 1) * 100
            else:
                percentile = 100
            measure = StatisticMeasure(statistic_journal=journal, source=interval, rank=rank, percentile=percentile)
            s.add(measure)
            measures.append(measure)
        if n > 8:  # avoid overlap in fuzzing (and also, plot individual points in this case)
            for q in range(5):
                measures[fuzz(n, q)].quartile = q
        self._log.debug('Ranked %s' % statistic)

    def _run_calculations(self, schedule):
        with self._db.session_context() as s:
            for start, finish in Interval.missing_dates(self._log, s, schedule, self):
                start_time, finish_time = local_date_to_time(start), local_date_to_time(finish)
                interval = add(s, Interval(start=start, finish=finish, schedule=schedule, owner=self))
                have_data = False
                for statistic_name in self._statistics_missing_summaries(s, start_time, finish_time):
                    data = [journal for journal in self._journal_data(s, statistic_name, start_time, finish_time)
                            if schedule.at_location(time_to_local_date(journal.time))]
                    if data:
                        summaries = [x for x in split(r'[\s,]*\[([^\]]+)\][\s ]*', statistic_name.summary) if x]
                        if summaries:
                            values = [x.value for x in data]
                            for summary in summaries:
                                self._create_value(s, interval, schedule, statistic_name, summary.lower(), data, values,
                                                   start_time)
                        else:
                            self._log.warn('Invalid summary for %s ("%s")' % (statistic_name, statistic_name.summary))
                        if 'msr' in summaries:
                            self._create_measures(s, interval, schedule, statistic_name, data)
                        have_data = True
                if have_data:
                    self._log.info('Added statistics for %s' % interval)
                else:
                    s.delete(interval)

    @classmethod
    def parse_name(cls, name):
        left, right = name.split(' ', 1)
        summary, period = left.split('/')
        return summary, period, right


def fuzz(n, q):
    i = (n-1) * q / 4
    if i != int(i):
        i = int(i) + choice([0, 1])  # if we're between two points, pick either
    return int(i)
