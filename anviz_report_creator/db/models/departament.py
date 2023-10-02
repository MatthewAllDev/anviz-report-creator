import sqlalchemy
from sqlalchemy.dialects import mssql as mssql_dialect

from anviz_report_creator.db.connection import session
from anviz_report_creator.db.models import Base


class Departament(Base):
    __tablename__: str = 'Dept'
    id: sqlalchemy.Column = sqlalchemy.Column('Deptid', mssql_dialect.INTEGER, primary_key=True)
    name: sqlalchemy.Column = sqlalchemy.Column('DeptName', mssql_dialect.VARCHAR(50))
    sup_departament_id: sqlalchemy.Column = sqlalchemy.Column('SupDeptid', mssql_dialect.INTEGER)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.id}, {self.sup_departament_id})>'

    @staticmethod
    def get_all() -> list:
        return session.query(Departament).all()

    @staticmethod
    def get(departament_id: int):
        return session.query(Departament).where(Departament.id == departament_id).first()

