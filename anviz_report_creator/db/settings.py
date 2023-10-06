class Settings:
    driver: str
    server: str
    database: str
    user: str
    password: str

    def __init__(self, driver: str = '{ODBC Driver 17 for SQL Server}', server: str = None,
                 database: str = None, user: str = None, password: str = None, validate: bool = True):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        if validate:
            self.validate()

    def validate(self):
        if self.driver == '':
            raise RuntimeError('Database driver ("driver") is not defined in config file')
        if self.server is None or self.server == '':
            raise RuntimeError('Database server ("server") is not defined in config file')
        if self.database is None or self.database == '':
            raise RuntimeError('Database name ("database") is not defined in config file')
        if self.user is None or self.user == '':
            raise RuntimeError('Database username ("user") is not defined in config file')
        if self.password is None or self.password == '':
            raise RuntimeError('Database user password ("password") is not defined in config file')
