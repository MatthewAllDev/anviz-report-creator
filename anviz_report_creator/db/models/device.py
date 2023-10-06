from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.models import Base


class Device(Base):
    __tablename__: str = 'FingerClient'
    id: Mapped[int] = mapped_column('Clientid', mssql_dialect.INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column('ClientName', mssql_dialect.VARCHAR(50))
    link_mode: Mapped[int] = mapped_column('Linkmode', mssql_dialect.SMALLINT)
    ip: Mapped[str] = mapped_column('IPaddress', mssql_dialect.VARCHAR(255))
    port: Mapped[int] = mapped_column('CommPort', mssql_dialect.INTEGER)
    client_number: Mapped[int] = mapped_column('ClientNumber', mssql_dialect.INTEGER)
    baud_rate: Mapped[int] = mapped_column('Baudrate', mssql_dialect.INTEGER)
    rec_status: Mapped[int] = mapped_column('RecStatus', mssql_dialect.INTEGER)
    floor_id: Mapped[int] = mapped_column('Floorid', mssql_dialect.INTEGER)
    machine_type: Mapped[int] = mapped_column('MachineType', mssql_dialect.INTEGER)
    device_type: Mapped[int] = mapped_column('DeviceType', mssql_dialect.INTEGER)
    comm_password: Mapped[str] = mapped_column('CommPWD', mssql_dialect.VARCHAR(50))
    device_flag: Mapped[int] = mapped_column('deviceflag', mssql_dialect.INTEGER)
    timezone: Mapped[str] = mapped_column('timezone', mssql_dialect.VARCHAR(255))

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.id})>'
