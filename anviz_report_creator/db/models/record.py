import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, select, ScalarResult
from sqlalchemy.sql.elements import and_, ColumnElement
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.models import Base
from anviz_report_creator.db.models import CheckType
from anviz_report_creator.db.models import Device
from anviz_report_creator.db.models import User
from anviz_report_creator.db.connection import connection


class Record(Base):
    __tablename__: str = 'Checkinout'
    id: Mapped[int] = mapped_column('Logid', mssql_dialect.INTEGER, primary_key=True)
    user_id: Mapped[str] = mapped_column('Userid', mssql_dialect.VARCHAR(20), ForeignKey('Userinfo.Userid'))
    user: Mapped['User'] = relationship('User')
    check_time: Mapped[datetime.datetime] = mapped_column('CheckTime', mssql_dialect.DATETIME)
    check_type_id: Mapped[int] = mapped_column('CheckType', mssql_dialect.INTEGER, ForeignKey('Status.Statusid'))
    check_type: Mapped['CheckType'] = relationship('CheckType')
    device_id: Mapped[int] = mapped_column('Sensorid', mssql_dialect.INTEGER, ForeignKey('FingerClient.Clientid'))
    device: Mapped['Device'] = relationship('Device')
    work_type_id: Mapped[int] = mapped_column('WorkType', mssql_dialect.INTEGER)
    identification_code: Mapped[int] = mapped_column('AttFlag', mssql_dialect.INTEGER)
    is_checked: Mapped[bool] = mapped_column('Checked', mssql_dialect.BIT)
    is_exported: Mapped[bool] = mapped_column('Exported', mssql_dialect.BIT)
    open_door_flag: Mapped[bool] = mapped_column('OpenDoorFlag', mssql_dialect.BIT)
    temperature: Mapped[float] = mapped_column('temperature', mssql_dialect.FLOAT)
    why_no_open: Mapped[int] = mapped_column('whynoopen', mssql_dialect.INTEGER)
    mask: Mapped[int] = mapped_column('mask', mssql_dialect.INTEGER)
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
        super().__init__()

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
    def get(record_id: int = None, user_ids: list = None, date_range: tuple = None) -> ScalarResult:
        conditions: list = []
        if record_id is not None:
            conditions.append(Record.id == record_id)
        if user_ids is not None:
            conditions.append(Record.user_id.in_(user_ids))
        if date_range is not None:
            finish_date: datetime.datetime = datetime.datetime.combine(date_range[1], datetime.datetime.min.time()) \
                                             + datetime.timedelta(days=1, microseconds=-1)
            conditions.append(Record.check_time.between(date_range[0], finish_date))
        condition: ColumnElement[bool] = and_(*conditions)
        return connection.get().scalars(select(Record).where(condition).order_by(Record.user_id, Record.check_time))
