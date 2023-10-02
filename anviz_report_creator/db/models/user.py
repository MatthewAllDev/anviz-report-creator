import sqlalchemy.orm
import sqlalchemy.sql.elements
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db import session
from anviz_report_creator.db.models import Base
from anviz_report_creator.db.models import Departament


class User(Base):
    __tablename__: str = 'Userinfo'
    id: sqlalchemy.Column = sqlalchemy.Column('Userid', mssql_dialect.VARCHAR(20), primary_key=True)
    code: sqlalchemy.Column = sqlalchemy.Column('UserCode', mssql_dialect.VARCHAR(20))
    name: sqlalchemy.Column = sqlalchemy.Column('Name', mssql_dialect.VARCHAR(50))
    sex: sqlalchemy.Column = sqlalchemy.Column('Sex', mssql_dialect.VARCHAR(10))
    password: sqlalchemy.Column = sqlalchemy.Column('Pwd', mssql_dialect.VARCHAR(50))
    departament_id: sqlalchemy.Column = sqlalchemy.Column('Deptid', mssql_dialect.INTEGER,
                                                          sqlalchemy.ForeignKey('Dept.Deptid'))
    departament: Departament = sqlalchemy.orm.relationship('Departament')
    nation: sqlalchemy.Column = sqlalchemy.Column('Nation', mssql_dialect.VARCHAR(50))
    birthday: sqlalchemy.Column = sqlalchemy.Column('Birthday', mssql_dialect.SMALLDATETIME)
    employ_date: sqlalchemy.Column = sqlalchemy.Column('EmployDate', mssql_dialect.SMALLDATETIME)
    phone: sqlalchemy.Column = sqlalchemy.Column('Telephone', mssql_dialect.VARCHAR(50))
    duty: sqlalchemy.Column = sqlalchemy.Column('Duty', mssql_dialect.VARCHAR(50))
    native_place: sqlalchemy.Column = sqlalchemy.Column('NativePlace', mssql_dialect.VARCHAR(50))
    id_card: sqlalchemy.Column = sqlalchemy.Column('IDCard', mssql_dialect.VARCHAR(50))
    address: sqlalchemy.Column = sqlalchemy.Column('Address', mssql_dialect.VARCHAR(150))
    mobile: sqlalchemy.Column = sqlalchemy.Column('Mobile', mssql_dialect.VARCHAR(50))
    educated: sqlalchemy.Column = sqlalchemy.Column('Educated', mssql_dialect.VARCHAR(50))
    polity: sqlalchemy.Column = sqlalchemy.Column('Polity', mssql_dialect.VARCHAR(50))
    specialty: sqlalchemy.Column = sqlalchemy.Column('Specialty', mssql_dialect.VARCHAR(50))
    is_att: sqlalchemy.Column = sqlalchemy.Column('IsAtt', mssql_dialect.BIT)
    is_over_time: sqlalchemy.Column = sqlalchemy.Column('Isovertime', mssql_dialect.BIT)
    is_rest: sqlalchemy.Column = sqlalchemy.Column('Isrest', mssql_dialect.BIT)
    remark: sqlalchemy.Column = sqlalchemy.Column('Remark', mssql_dialect.VARCHAR(250))
    mg_flag: sqlalchemy.Column = sqlalchemy.Column('MgFlag', mssql_dialect.SMALLINT)
    card_num: sqlalchemy.Column = sqlalchemy.Column('CardNum', mssql_dialect.VARCHAR(10))
    picture: sqlalchemy.Column = sqlalchemy.Column('Picture', mssql_dialect.IMAGE)
    user_flag: sqlalchemy.Column = sqlalchemy.Column('UserFlag', mssql_dialect.INTEGER)
    group_id: sqlalchemy.Column = sqlalchemy.Column('Groupid', mssql_dialect.INTEGER)
    class_flag: sqlalchemy.Column = sqlalchemy.Column('ClassFlag', mssql_dialect.INTEGER)
    other_info: sqlalchemy.Column = sqlalchemy.Column('OtherInfo', mssql_dialect.IMAGE)
    admin_group_id: sqlalchemy.Column = sqlalchemy.Column('admingroupid', mssql_dialect.INTEGER)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.departament.name}, {self.id})>'

    @staticmethod
    def get(user_id: int = None, departament_id: int = None) -> list:
        conditions: list = []
        if user_id is not None:
            conditions.append(User.id == user_id)
        if departament_id is not None:
            conditions.append(User.departament_id == departament_id)
        condition: sqlalchemy.sql.elements.BooleanClauseList or sqlalchemy.sql.elements.BinaryExpression = \
            sqlalchemy.sql.and_(*conditions)
        return session.query(User).where(condition).all()

    @staticmethod
    def get_ids(departament_id: int = None) -> list:
        user_ids: list = []
        users: list = User.get(departament_id=departament_id)
        for user in users:
            user_ids.append(user.id)
        return user_ids
