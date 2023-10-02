import sqlalchemy.orm
from sqlalchemy.dialects import mssql as mssql_dialect
from anviz_report_creator.db.models import Base


class Device(Base):
    __tablename__: str = 'FingerClient'
    id: sqlalchemy.Column = sqlalchemy.Column('Clientid', mssql_dialect.INTEGER, primary_key=True)
    name: sqlalchemy.Column = sqlalchemy.Column('ClientName', mssql_dialect.VARCHAR(50))
    link_mode: sqlalchemy.Column = sqlalchemy.Column('Linkmode', mssql_dialect.SMALLINT)
    ip: sqlalchemy.Column = sqlalchemy.Column('IPaddress', mssql_dialect.VARCHAR(255))
    port: sqlalchemy.Column = sqlalchemy.Column('CommPort', mssql_dialect.INTEGER)
    client_number: sqlalchemy.Column = sqlalchemy.Column('ClientNumber', mssql_dialect.INTEGER)
    baud_rate: sqlalchemy.Column = sqlalchemy.Column('Baudrate', mssql_dialect.INTEGER)
    rec_status: sqlalchemy.Column = sqlalchemy.Column('RecStatus', mssql_dialect.INTEGER)
    floor_id: sqlalchemy.Column = sqlalchemy.Column('Floorid', mssql_dialect.INTEGER)
    machine_type: sqlalchemy.Column = sqlalchemy.Column('MachineType', mssql_dialect.INTEGER)
    device_type: sqlalchemy.Column = sqlalchemy.Column('DeviceType', mssql_dialect.INTEGER)
    comm_password: sqlalchemy.Column = sqlalchemy.Column('CommPWD', mssql_dialect.VARCHAR(50))
    device_flag: sqlalchemy.Column = sqlalchemy.Column('deviceflag', mssql_dialect.INTEGER)
    timezone: sqlalchemy.Column = sqlalchemy.Column('timezone', mssql_dialect.VARCHAR(255))

    def __repr__(self) -> str:
        return f'<{type(self).__name__}({self.name}, {self.id})>'
