
from json import dumps

from pendulum.tz import get_local_timezone
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from ch2.lib.data import assert_attr
from .source import SourceType, Source
from .statistic import StatisticJournal, STATISTIC_JOURNAL_CLASSES, StatisticName
from ..support import Base
from ..types import Date, Cls, Json, Sched, Sort
from ...lib.date import local_date_to_time
from ...lib.schedule import Schedule
from ...squeal.tables.constant import SystemConstant

TIMEZONE = 'timezone'


class Topic(Base):

    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('topic.id'), nullable=True)
    # http://docs.sqlalchemy.org/en/latest/orm/self_referential.html
    children = relationship('Topic', backref=backref('parent', remote_side=[id]))
    schedule = Column(Sched, nullable=False)
    start = Column(Date)
    finish = Column(Date)
    name = Column(Text, nullable=False, server_default='')
    description = Column(Text, nullable=False, server_default='')
    sort = Column(Sort, nullable=False, server_default='')

    def __init__(self, id=None, parent=None, parent_id=None, schedule=None, name=None, description=None, sort=None):
        # Topic instances are only created in config.  so we intercept here to
        # duplicate data for start and finish - it's not needed elsewhere.
        if not isinstance(schedule, Schedule):
            schedule = Schedule(schedule)
        self.id = id
        self.parent = parent
        self.parent_id = parent_id
        self.schedule = schedule
        self.name = name
        self.description = description
        self.sort = sort
        self.start = schedule.start
        self.finish = schedule.finish

    def __str__(self):
        return 'Topic "%s" (%s)' % (self.name, self.schedule)

    def populate(self, s, date):
        self.journal = s.query(TopicJournal). \
            filter(TopicJournal.topic == self,
                   TopicJournal.time == date).one_or_none()
        if not self.journal:
            self.journal = TopicJournal(topic=self, time=date)
            s.add(self.journal)


class TopicField(Base):

    __tablename__ = 'topic_field'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id', ondelete='cascade'), nullable=False)
    topic = relationship('Topic',
                         backref=backref('fields', cascade='all, delete-orphan',
                                         passive_deletes=True,
                                         order_by='TopicField.sort'))
    type = Column(Integer, nullable=False)  # StatisticJournalType
    sort = Column(Sort)
    statistic_name_id = Column(Integer, ForeignKey('statistic_name.id', ondelete='cascade'), nullable=False)
    statistic_name = relationship('StatisticName')
    display_cls = Column(Cls, nullable=False)
    display_args = Column(Json, nullable=False, server_default=dumps(()))
    display_kargs = Column(Json, nullable=False, server_default=dumps({}))
    schedule = Column(Sched, nullable=False, server_default='')

    def __str__(self):
        return 'TopicField "%s"/"%s"' % (self.topic.name, self.statistic_name.name)


class TopicJournal(Source):

    __tablename__ = 'topic_journal'

    id = Column(Integer, ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship('Topic')
    date = Column(Date, nullable=False, index=True)

    __mapper_args__ = {
        'polymorphic_identity': SourceType.TOPIC
    }

    def populate(self, log, s):
        if hasattr(self, 'statistics'):
            return
        assert_attr(self, 'time', 'date')
        if self.id is None:
            s.flush()
        log.debug('Populating journal for topic %s at %s' % (self.topic.name, self.time))
        self.statistics = {}
        for field in self.topic.fields:
            assert_attr(field, 'schedule')
            if field.schedule.at_location(self.date):
                log.debug('Finding StatisticJournal for field %s' % field.statistic_name.name)
                journal = s.query(StatisticJournal).join(StatisticName, Source). \
                    filter(StatisticJournal.statistic_name == field.statistic_name,
                           Source.time == self.time,
                           StatisticName.owner == self.topic,
                           StatisticName.constraint == self.topic.id).one_or_none()
                if not journal:
                    journal = STATISTIC_JOURNAL_CLASSES[field.type](statistic_name=field.statistic_name, source=self)
                    s.add(journal)
                self.statistics[field] = journal

    def __str__(self):
        return 'TopicJournal from %s' % self.date

    @classmethod
    def check_tz(cls, db):
        from ...squeal.database import add
        with db.session_context() as s:
            tz = get_local_timezone()
            db_tz = s.query(SystemConstant).filter(SystemConstant.name == TIMEZONE).one_or_none()
            if not db_tz:
                db_tz = add(s, SystemConstant(name=TIMEZONE, value=''))
            if db_tz.value != tz.name:
                cls.__reset_timezone(s)
                db_tz.value = tz.name

    @classmethod
    def __reset_timezone(cls, s):
        for tj in s.query(TopicJournal).all():
            tj.time = local_date_to_time(tj.date)
