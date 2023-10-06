class Settings:
    transfer_protocol: str
    api_url: str
    api_version: str
    public_keys: list

    def __init__(self, transfer_protocol: str = 'https', api_url: str = 'api.ilovepdf.com',
                 api_version: str = 'v1', public_keys: list = None, validate: bool = True):
        self.transfer_protocol = transfer_protocol
        self.api_url = api_url
        self.api_version = api_version
        self.public_keys = public_keys
        if validate:
            self.validate()

    def validate(self):
        if self.transfer_protocol == '':
            raise RuntimeError('iLovePDF API transfer protocol ("transfer_protocol") is not defined in config file')
        if self.api_url == '':
            raise RuntimeError('iLovePDF API URL ("api_url") is not defined in config file')
        if self.api_version == '':
            raise RuntimeError('iLovePDF API version ("api_version") is not defined in config file')
        if self.public_keys is None or len(self.public_keys) == 0:
            raise RuntimeError('iLovePDF API keys ("public_keys") is not defined in config file')
