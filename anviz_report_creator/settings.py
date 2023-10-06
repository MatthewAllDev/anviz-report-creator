from .db import Settings as DBSettings
from .excel_to_pdf_convertor import APISettings as ConvertorAPISettings
from os.path import exists
import json


class Settings:
    db: DBSettings
    convertor: ConvertorAPISettings
    __config_file_path: str
    __is_convertor_used: bool

    def __init__(self, config_file_path: str = 'config.json', is_convertor_used: bool = True):
        self.set_default_settings()
        self.__config_file_path: str = config_file_path
        self.__is_convertor_used: bool = is_convertor_used
        if not exists(config_file_path):
            self.save_settings()
        else:
            self.load_settings()
        pass

    def load_settings(self):
        with open(self.__config_file_path, 'r', encoding='utf-8') as file:
            settings_data: dict = json.load(file)
            for key, value in settings_data.items():
                if not hasattr(self, key):
                    continue
                setattr(self, key, type(getattr(self, key))(**value))

    def save_settings(self):
        with open(self.__config_file_path, 'w', encoding='utf-8') as file:
            json.dump(self, file, indent=4,
                      default=lambda o: dict(filter(lambda i: False if i[0][0:1] == '_' else True, o.__dict__.items())))

    def set_default_settings(self):
        self.db = DBSettings(server='', database='', user='', password='', validate=False)
        self.convertor = ConvertorAPISettings(public_keys=[], validate=False)
