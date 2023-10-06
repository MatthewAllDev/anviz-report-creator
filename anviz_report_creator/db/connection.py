import sqlalchemy
from sqlalchemy.orm import Session
from .settings import Settings


class Connection:
    settings: Settings = None
    engine: sqlalchemy.engine.Engine
    sessions: list[Session]

    def __init__(self, settings: Settings = None):
        self.sessions = []
        if settings is not None:
            self.init(settings)

    def init(self, settings: Settings):
        self.close()
        self.settings = settings
        self.create_engine()
        self.add_session()

    def get(self, index: int = -1) -> Session:
        if not len(self.sessions):
            if self.settings is None:
                raise RuntimeError('You have not initialized the connection yet, to initialize call the method '
                                   '"Connection.init(settings: db.Settings)".')
            else:
                raise RuntimeError('There are no active sessions, please create a session by calling the method'
                                   '"Connection.add_session()')
        return self.sessions[index]

    def create_engine(self):
        self.close()
        self.engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect='
                                               f'DRIVER={self.settings.driver};'
                                               f'SERVER={self.settings.server};'
                                               f'DATABASE={self.settings.database};'
                                               f'UID={self.settings.user};'
                                               f'PWD={self.settings.password}')

    def add_session(self) -> Session:
        session: Session = Session(self.engine)
        self.sessions.append(session)
        return session

    def close(self):
        while len(self.sessions) > 0:
            session: Session = self.sessions.pop()
            session.close()

    def close_session(self, session: Session):
        try:
            index: int = self.sessions.index(session)
        except ValueError:
            return
        session = self.sessions.pop(index)
        session.close()


connection: Connection = Connection()
