from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.connection import connection
from anviz_report_creator.db.models import Base


class Departament(Base):
    __tablename__: str = 'Dept'
    id: Mapped[int] = mapped_column('Deptid', mssql_dialect.INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column('DeptName', mssql_dialect.VARCHAR(50))
    sup_departament_id: Mapped[int] = mapped_column('SupDeptid', mssql_dialect.INTEGER)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.id}, {self.sup_departament_id})>'

    @staticmethod
    def get_all() -> ScalarResult:
        return connection.get().scalars(select(Departament))

    @staticmethod
    def get(departament_id: int) -> 'Departament':
        return connection.get().scalars(select(Departament).where(Departament.id == departament_id)).one()
