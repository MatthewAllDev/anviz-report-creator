import sqlalchemy
from sqlalchemy.orm import sessionmaker
from anviz_report_creator.config import db as config

engine: sqlalchemy.engine.Engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect='
                                                            f'DRIVER={config.driver};'
                                                            f'SERVER={config.server};'
                                                            f'DATABASE={config.database};'
                                                            f'UID={config.user};'
                                                            f'PWD={config.password}', encoding='utf-8')
Session: sqlalchemy.orm.sessionmaker = sessionmaker(bind=engine)
session: sqlalchemy.orm.Session = Session()
