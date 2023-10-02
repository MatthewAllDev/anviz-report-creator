import datetime
import sqlalchemy.orm
import sqlalchemy.sql.elements
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.models import Base
from anviz_report_creator.db.models import CheckType
from anviz_report_creator.db.models import Device
from anviz_report_creator.db.models import User
from anviz_report_creator.db.connection import session


class Record(Base):
    __tablename__: str = 'Checkinout'
    id: sqlalchemy.Column = sqlalchemy.Column('Logid', mssql_dialect.INTEGER, primary_key=True)
    user_id: sqlalchemy.Column = sqlalchemy.Column('Userid', mssql_dialect.VARCHAR(20),
                                                   sqlalchemy.ForeignKey('Userinfo.Userid'))
    user: User = sqlalchemy.orm.relationship('User')
    check_time: sqlalchemy.Column = sqlalchemy.Column('CheckTime', mssql_dialect.DATETIME)
    check_type_id: sqlalchemy.Column = sqlalchemy.Column('CheckType', mssql_dialect.INTEGER,
                                                         sqlalchemy.ForeignKey('Status.Statusid'))
    check_type: CheckType = sqlalchemy.orm.relationship('CheckType')
    device_id: sqlalchemy.Column = sqlalchemy.Column('Sensorid', mssql_dialect.INTEGER,
                                                     sqlalchemy.ForeignKey('FingerClient.Clientid'))
    device: Device = sqlalchemy.orm.relationship('Device')
    work_type_id: sqlalchemy.Column = sqlalchemy.Column('WorkType', mssql_dialect.INTEGER)
    identification_code: sqlalchemy.Column = sqlalchemy.Column('AttFlag', mssql_dialect.INTEGER)
    is_checked: sqlalchemy.Column = sqlalchemy.Column('Checked', mssql_dialect.BIT)
    is_exported: sqlalchemy.Column = sqlalchemy.Column('Exported', mssql_dialect.BIT)
    open_door_flag: sqlalchemy.Column = sqlalchemy.Column('OpenDoorFlag', mssql_dialect.BIT)
    temperature: sqlalchemy.Column = sqlalchemy.Column('temperature', mssql_dialect.FLOAT)
    why_no_open: sqlalchemy.Column = sqlalchemy.Column('whynoopen', mssql_dialect.INTEGER)
    mask: sqlalchemy.Column = sqlalchemy.Column('mask', mssql_dialect.INTEGER)
    is_error_record: bool = False
    is_warning_record: bool = False
    error_reason: str = ''

    def __init__(self,
                 user_id: str,
                 check_time: datetime.datetime,
                 check_type_id: int,
                 device_id: int,
                 work_type_id: int = 0,
                 identification_code: int = 19,
                 is_checked: bool = False,
                 is_exported: bool = False,
                 open_door_flag: bool = False,
                 temperature: float = 0.0,
                 why_no_open: int = 0,
                 mask: int = 2):
        self.user_id: str = user_id
        self.check_time: datetime.datetime = check_time
        self.check_type_id: int = check_type_id
        self.device_id: int = device_id
        self.work_type_id: int = work_type_id
        self.identification_code: int = identification_code
        self.is_checked: bool = is_checked
        self.is_exported: bool = is_exported
        self.open_door_flag: bool = open_door_flag
        self.temperature: float = temperature
        self.why_no_open: int = why_no_open
        self.mask: int = mask

    def __repr__(self) -> str:
        return f'<{type(self).__name__}' \
               f'({self.user.name}, ' \
               f'{self.check_time}, ' \
               f'{self.check_type.name}' \
               f'{", Error record" if self.is_error_record else ""}' \
               f'{", Warning record" if self.is_warning_record else ""}' \
               f'{f": {self.error_reason}" if self.is_error_record or self.is_warning_record else ""})>'

    def __iter__(self):
        yield self.id
        yield f'{self.user.name} ({self.user_id})'
        yield self.check_time
        yield self.check_type.name
        if self.device is not None:
            yield self.device.name
        else:
            yield ''
        yield self.error_reason if self.is_error_record or self.is_warning_record else ""

    @staticmethod
    def get(record_id: int = None, user_ids: list = None, date_range: tuple = None) -> list:
        conditions: list = []
        if record_id is not None:
            conditions.append(Record.id == record_id)
        if user_ids is not None:
            conditions.append(Record.user_id.in_(user_ids))
        if date_range is not None:
            finish_date: datetime.datetime = datetime.datetime.combine(date_range[1], datetime.datetime.min.time())\
                                             + datetime.timedelta(days=1, microseconds=-1)
            conditions.append(Record.check_time.between(date_range[0], finish_date))
        condition: sqlalchemy.sql.elements.BooleanClauseList or sqlalchemy.sql.elements.BinaryExpression = \
            sqlalchemy.sql.and_(*conditions)
        return session.query(Record).where(condition).order_by(Record.user_id, Record.check_time).all()
