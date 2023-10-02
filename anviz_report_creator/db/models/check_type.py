import sqlalchemy.orm
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.models import Base


class CheckType(Base):
    __tablename__: str = 'Status'
    id: sqlalchemy.Column = sqlalchemy.Column('Statusid', mssql_dialect.INTEGER, primary_key=True)
    char: sqlalchemy.Column = sqlalchemy.Column('StatusChar', mssql_dialect.VARCHAR(2))
    name: sqlalchemy.Column = sqlalchemy.Column('StatusText', mssql_dialect.VARCHAR(50))

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.id})>'
