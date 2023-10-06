import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, select, ScalarResult
from sqlalchemy.sql.elements import and_, ColumnElement
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.connection import connection
from anviz_report_creator.db.models import Base
from anviz_report_creator.db.models import Departament


class User(Base):
    __tablename__: str = 'Userinfo'
    id: Mapped[str] = mapped_column('Userid', mssql_dialect.VARCHAR(20), primary_key=True)
    code: Mapped[str] = mapped_column('UserCode', mssql_dialect.VARCHAR(20))
    name: Mapped[str] = mapped_column('Name', mssql_dialect.VARCHAR(50))
    sex: Mapped[str] = mapped_column('Sex', mssql_dialect.VARCHAR(10))
    password: Mapped[str] = mapped_column('Pwd', mssql_dialect.VARCHAR(50))
    departament_id: Mapped[str] = mapped_column('Deptid', mssql_dialect.INTEGER, ForeignKey('Dept.Deptid'))
    departament: Mapped['Departament'] = relationship('Departament')
    nation: Mapped[str] = mapped_column('Nation', mssql_dialect.VARCHAR(50))
    birthday: Mapped[datetime.datetime] = mapped_column('Birthday', mssql_dialect.SMALLDATETIME)
    employ_date: Mapped[datetime.datetime] = mapped_column('EmployDate', mssql_dialect.SMALLDATETIME)
    phone: Mapped[str] = mapped_column('Telephone', mssql_dialect.VARCHAR(50))
    duty: Mapped[str] = mapped_column('Duty', mssql_dialect.VARCHAR(50))
    native_place: Mapped[str] = mapped_column('NativePlace', mssql_dialect.VARCHAR(50))
    id_card: Mapped[str] = mapped_column('IDCard', mssql_dialect.VARCHAR(50))
    address: Mapped[str] = mapped_column('Address', mssql_dialect.VARCHAR(150))
    mobile: Mapped[str] = mapped_column('Mobile', mssql_dialect.VARCHAR(50))
    educated: Mapped[str] = mapped_column('Educated', mssql_dialect.VARCHAR(50))
    polity: Mapped[str] = mapped_column('Polity', mssql_dialect.VARCHAR(50))
    specialty: Mapped[str] = mapped_column('Specialty', mssql_dialect.VARCHAR(50))
    is_att: Mapped[bool] = mapped_column('IsAtt', mssql_dialect.BIT)
    is_over_time: Mapped[bool] = mapped_column('Isovertime', mssql_dialect.BIT)
    is_rest: Mapped[bool] = mapped_column('Isrest', mssql_dialect.BIT)
    remark: Mapped[str] = mapped_column('Remark', mssql_dialect.VARCHAR(250))
    mg_flag: Mapped[int] = mapped_column('MgFlag', mssql_dialect.SMALLINT)
    card_num: Mapped[str] = mapped_column('CardNum', mssql_dialect.VARCHAR(10))
    picture: Mapped[bytes] = mapped_column('Picture', mssql_dialect.IMAGE)
    user_flag: Mapped[int] = mapped_column('UserFlag', mssql_dialect.INTEGER)
    group_id: Mapped[int] = mapped_column('Groupid', mssql_dialect.INTEGER)
    class_flag: Mapped[int] = mapped_column('ClassFlag', mssql_dialect.INTEGER)
    other_info: Mapped[bytes] = mapped_column('OtherInfo', mssql_dialect.IMAGE)
    admin_group_id: Mapped[int] = mapped_column('admingroupid', mssql_dialect.INTEGER)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.departament.name}, {self.id})>'

    @staticmethod
    def get(user_id: int = None, departament_id: int = None) -> ScalarResult:
        conditions: list = []
        if user_id is not None:
            conditions.append(User.id == user_id)
        if departament_id is not None:
            conditions.append(User.departament_id == departament_id)
        condition: ColumnElement[bool] = and_(*conditions)
        return connection.get().scalars(select(User).where(condition))

    @staticmethod
    def get_ids(departament_id: int = None) -> list:
        user_ids: list = []
        users: ScalarResult = User.get(departament_id=departament_id)
        for user in users:
            user_ids.append(user.id)
        return user_ids
