
from ..command.args import DATE, NAME, VALUE, DELETE, FORCE, mm, COMMAND, CONSTANTS, SET
from ..squeal.database import add
from ..squeal.tables.constant import Constant, ConstantJournal
from ..squeal.tables.statistic import StatisticJournal, StatisticName, STATISTIC_JOURNAL_CLASSES


def constants(args, log, db):
    '''
# constant

    ch2 constants [NAME [DATE]]

Lists constants to stdout.

    ch2 constants --set NAME [DATE] VALUE

Defines a new entry.  If date is omitted a single value is used for all time.

    ch2 constants --delete NAME [DATE]

Deletes an entry.

ActivityGroup names can be matched by SQL patterns.  So FTHR.% matches both FTHR.Run and FTHR.Bike, for example.
In such a case "entry" in the descriptions above may refer to multiple entries.
    '''
    name, date, value, set, delete, force = args[NAME], args[DATE], args[VALUE], args[SET], args[DELETE], args[FORCE]
    with db.session_context() as s:
        if name:
            constants = constants_like(log, s, name)
            if not constants:
                raise Exception('Name "%s" matched no entries (see `%s %s`)' % (name, COMMAND, CONSTANTS))
        else:
            constants = []
        if set:
            # date is the optional entry for set
            if date and not value:
                date, value = None, date
            if not name or not value:
                raise Exception('%s requires name and value' % mm(SET))
            set_constants(log, s, constants, date, value, force)
        elif delete:
            if not name:
                raise Exception('%s requires at least a name' % mm(DELETE))
            if value:
                raise Exception('Do not provide a value when deleting Constants')
            if not date and not force:
                raise Exception('Use %s to delete all entries for a Constant' % mm(FORCE))
            delete_constants(log, s, constants, date)
        else:
            if value:
                raise Exception('Do not provide a value when printing Constants')
            print_constants(log, s, constants, name, date)


def constants_like(log, s, name):
    constant = s.query(Constant).filter(Constant.name.like(name)).order_by(Constant.name).all()
    if not constant:
        constants = s.query(Constant).all()
        if constants:
            log.info('Available constants:')
            for constant in constants:
                log.info('%s - %s' % (constant.statistic_name.name, constant.statistic_name.description))
        else:
            log.error('No constants defined - configure system correctly')
        raise Exception('Constant "%s" is not defined' % name)
    return constant


def set_constants(log, s, constants, date, value, force):
    if not date:
        log.info('Checking any previous values')
        journals = []
        for constant in constants:
            journals += s.query(ConstantJournal).join(StatisticJournal, StatisticName, Constant). \
                filter(Constant.id == constant.id).all()
        if journals:
            log.info('Need to delete %d ConstantJournal entries' % len(journals))
            if not force:
                raise Exception('Use %s to confirm deletion of prior values' % mm(FORCE))
            for journal in journals:
                s.delete(journal)
        date = '1970-01-01'
    for constant in constants:
        cjournal = add(s, ConstantJournal(time=date))
        add(s, STATISTIC_JOURNAL_CLASSES[constant.type](
            statistic_name=constant.statistic_name, source=cjournal, value=value))
        log.info('Added value %s at %s for %s' % (value, date, constant.name))
    log.warn('You may want to (re-)calculate statistics')


def delete_constants(log, s, constants, date):
    if date:
        for constant in constants:
            for repeat in range(2):
                journal = s.query(ConstantJournal).join(StatisticJournal, StatisticName, Constant). \
                    filter(Constant.id == constant.id,
                           ConstantJournal.time == date).one_or_none()
                if repeat:
                    log.info('Deleting %s on %s' % (constant.name, journal.time))
                    s.delete(journal)
                else:
                    if not journal:
                        raise Exception('No entry for %s on %s' % (constant.name, date))
    else:
        for constant in constants:
            for journal in s.query(ConstantJournal).join(StatisticJournal, StatisticName, Constant). \
                    filter(Constant.id == constant.id).order_by(ConstantJournal.time).all():
                log.info('Deleting %s on %s' % (constant.name, journal.time))
                s.delete(journal)


def print_constants(log, s, constants, name, date):
    if not constants:
        constants = s.query(Constant).order_by(Constant.name).all()
        if not constants:
            raise Exception('No Constants defined - configure system')
    print()
    for constant in constants:
        if not date:
            print('%s: %s' % (constant.name,
                              constant.statistic_name.description
                              if constant.statistic_name.description else '[no description]'))
            if name:  # only print values if we're not listing all
                found = False
                for journal in s.query(StatisticJournal).join(ConstantJournal, StatisticName, Constant). \
                        filter(Constant.id == constant.id).order_by(ConstantJournal.time).all():
                    print('%s: %s' % (journal.time, journal.value))
                    found = True
                if not found:
                    log.warn('No values found for %s' % constant.name)
            print()
        else:
            journal = ConstantJournal.lookup_statistic_journal(log, s, constant.name,
                                                               constant.statistic_name.constraint, date)
            if journal:
                print('%s %s %s' % (constant.name, journal.source.time, journal.value))
            else:
                log.warn('No values found for %s' % constant.name)

