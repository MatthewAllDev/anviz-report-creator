from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.models import Base


class CheckType(Base):
    __tablename__: str = 'Status'
    id: Mapped[int] = mapped_column('Statusid', mssql_dialect.INTEGER, primary_key=True)
    char: Mapped[str] = mapped_column('StatusChar', mssql_dialect.VARCHAR(2))
    name: Mapped[str] = mapped_column('StatusText', mssql_dialect.VARCHAR(50))

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.id})>'
