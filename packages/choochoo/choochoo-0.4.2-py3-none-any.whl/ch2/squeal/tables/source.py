
from enum import IntEnum

from sqlalchemy import ForeignKey, Column, Integer, func, and_, distinct
from sqlalchemy.event import listens_for, remove
from sqlalchemy.orm import Session, aliased

from ..support import Base
from ..types import Time, OpenSched, Owner, Date
from ...lib.date import to_time, time_to_local_date


class SourceType(IntEnum):

    SOURCE = 0
    INTERVAL = 1
    ACTIVITY = 2
    TOPIC = 3
    CONSTANT = 4
    MONITOR = 5


class Source(Base):

    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    time = Column(Time, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': SourceType.SOURCE,
        'polymorphic_on': type
    }

    @classmethod
    def before_flush(cls, session):
        cls.__clean_dirty_intervals(session)

    @classmethod
    def __clean_dirty_intervals(cls, session):
        from .statistic import StatisticJournal
        from .topic import TopicJournal
        times = set()
        # all sources except intervals that are being deleted
        times |= set(instance.time for instance in session.deleted
                     if isinstance(instance, Source) and not isinstance(instance, Interval) and instance.time)
        # all modified sources except intervals
        times |= set(instance.time for instance in session.dirty
                     if isinstance(instance, Source) and not isinstance(instance, Interval)
                     and session.is_modified(instance) and instance.time)
        # if any modified statistic journals are associated with an existing topic journal, include that
        # this handles the case where a user edits something in the diaty
        for instance in session.dirty:
            # is it a subclass of StatisticJournal?
            if isinstance(instance, StatisticJournal) and type(instance) != StatisticJournal:
                if session.is_modified(instance) and isinstance(instance.source, TopicJournal):
                    times.add(instance.source.time)
        # all new sources except intervals and topic journals (the latter are handled below)
        times |= set(instance.time for instance in session.new
                     if isinstance(instance, Source) and not isinstance(instance, Interval)
                     and not isinstance(instance, TopicJournal) and instance.time)
        # include new topic journals only if they have non-null data
        # this handles the case where an empty diary entry is viewed
        for instance in session.new:
            # is it a subclass of StatisticJournal?
            if isinstance(instance, StatisticJournal) and type(instance) != StatisticJournal:
                if instance.value is not None:
                    if instance.source and isinstance(instance.source, TopicJournal) and instance.source.time:
                        times.add(instance.source.time)
        if times:
            cls.clean_times(session, times)

    @classmethod
    def clean_times(cls, session, times):
        schedules = [schedule[0] for schedule in session.query(distinct(Interval.schedule)).all()]
        for time in times:
            date = time_to_local_date(to_time(time))
            for schedule in schedules:
                start = schedule.start_of_frame(date)
                finish = schedule.next_frame(date)
                for interval in session.query(Interval). \
                        filter(Interval.finish >= start,
                               Interval.start < finish,
                               Interval.schedule == schedule).all():
                    session.delete(interval)


@listens_for(Session, 'before_flush')
def before_flush(session, context, instances):
    Source.before_flush(session)


class Interval(Source):

    __tablename__ = 'interval'

    id = Column(Integer, ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    schedule = Column(OpenSched, nullable=False, index=True)
    # disambiguate creator so each can wipe only its own data on force
    owner = Column(Owner, nullable=False)
    # these are for the schedule - finish is redundant (start is not because of timezone issues)
    start = Column(Date, nullable=False, index=True)
    finish = Column(Date, nullable=False, index=True)

    __mapper_args__ = {
        'polymorphic_identity': SourceType.INTERVAL
    }

    def __str__(self):
        return 'Interval "%s from %s" (owner %d)' % \
               (self.schedule, self.start, Owner().process_literal_param(self.owner, None))

    @classmethod
    def _missing_interval_starts(cls, log, s, schedule, owner):
        stats_start, stats_finish = cls._raw_statistics_time_range(s)
        log.debug('Statistics exist %s - %s' % (stats_start, stats_finish))
        starts = cls._open_intervals(s, schedule, owner)
        stats_start_date = time_to_local_date(stats_start)
        if not cls._get_interval(s, schedule, owner, stats_start_date):
            starts = [schedule.start_of_frame(stats_start_date)] + starts
        log.debug('Have %d open blocks finishing at %s' % (len(starts), stats_finish))
        return starts, stats_finish

    @classmethod
    def _raw_statistics_time_range(cls, s):
        from .statistic import StatisticJournal, StatisticName
        start, finish = s.query(func.min(Source.time), func.max(Source.time)). \
            outerjoin(StatisticJournal). \
            filter(StatisticName.id != None,
                   Source.time > to_time(0.0)).one()
        if start and finish:
            return start, finish
        else:
            raise Exception('No statistics are currently defined')

    @classmethod
    def _open_intervals(cls, s, schedule, owner):
        close = aliased(Interval)
        return [result[0] for result in s.query(Interval.finish). \
            outerjoin(close,
                      and_(Interval.finish == close.start,
                           Interval.owner == close.owner,
                           Interval.schedule == close.schedule)). \
            filter(close.start == None,
                   Interval.owner == owner,
                   Interval.schedule == schedule). \
            order_by(Interval.finish).all()]

    @classmethod
    def _get_interval(cls, s, schedule, owner, start):
        return s.query(Interval). \
            filter(Interval.start == start,
                   Interval.schedule == schedule,
                   Interval.owner == owner).one_or_none()

    @classmethod
    def _missing_intervals_from(cls, log, s, schedule, owner, start, finish):
        while start <= time_to_local_date(finish):
            next = schedule.next_frame(start)
            log.debug('Missing Interval %s - %s' % (start, next))
            yield start, next
            start = next
            if cls._get_interval(s, schedule, owner, start):
                return

    @classmethod
    def missing(cls, log, s, schedule, owner):
        starts, overall_finish = cls._missing_interval_starts(log, s, schedule, owner)
        for block_start in starts:
            yield from cls._missing_intervals_from(log, s, schedule, owner, block_start, overall_finish)
