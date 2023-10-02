import os
import aiohttp
from anviz_report_creator.config import ilovepdf_api as config


class API:
    def __init__(self, tool: str):
        self.__transfer_protocol: str = config.transfer_protocol if config.transfer_protocol else 'https'
        self.__api_url: str = config.api_url if config.api_url else 'api.ilovepdf.com'
        self.__api_version: str = config.api_version if config.api_version else 'v1'
        self.__tool: str = tool
        self.__public_keys: str or list = config.public_keys
        self.__public_key: str = self.__get_public_key()
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.__is_authenticated: bool = False
        self.__task: str or None = None
        self.__server: str or None = None
        self.uploaded_files: list = []

    async def authenticate(self):
        response: aiohttp.ClientResponse = await self.__session.post(f'{self.__transfer_protocol}://'
                                                                     f'{self.__api_url}/{self.__api_version}/auth',
                                                                     data={'public_key': self.__public_key})
        response_data: dict = await response.json()
        await self.close_session()
        self.__session = aiohttp.ClientSession(headers={'Authorization': f'Bearer {response_data["token"]}'})
        self.__is_authenticated = True

    async def create_task(self) -> dict:
        if not self.__is_authenticated:
            await self.authenticate()
        response: aiohttp.ClientResponse = await self.__session.get(f'{self.__transfer_protocol}://'
                                                                    f'{self.__api_url}/{self.__api_version}'
                                                                    f'/start/{self.__tool}')
        response_data: dict = await response.json()
        if response_data.get('name') == 'Unauthorized':
            try:
                self.__public_key: str = self.__get_public_key()
            finally:
                await self.close_session()
            return await self.create_task()
        self.__task: str = response_data['task']
        self.__server: str = response_data["server"]
        return response_data

    async def upload_file(self, file_path: str) -> dict:
        file_name: str = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            response: aiohttp.ClientResponse = await self.__session.post(f'{self.__transfer_protocol}://'
                                                                         f'{self.__server}/{self.__api_version}'
                                                                         f'/upload',
                                                                         data={
                                                                             'task': self.__task,
                                                                             'file': file
                                                                         })
            response_data: dict = await response.json()
            response_data['filename'] = file_name
            self.uploaded_files.append(response_data)
            return response_data

    async def process(self, files: list or dict = None) -> dict:
        if files is None:
            files = self.uploaded_files
        prepared_files: dict = {}
        if type(files) == dict:
            files = [files]
        for index, file in enumerate(files):
            file: dict
            for key, value in file.items():
                prepared_files[f'files[{index}][{key}]'] = value
        data = {
            'task': self.__task,
            'tool': self.__tool
        }
        data = data | prepared_files
        response: aiohttp.ClientResponse = await self.__session.post(f'{self.__transfer_protocol}://'
                                                                     f'{self.__server}/{self.__api_version}'
                                                                     f'/process',
                                                                     data=data)
        response_data: dict = await response.json()
        return response_data

    async def download(self, output_path: str) -> str:
        response: aiohttp.ClientResponse = await self.__session.get(f'{self.__transfer_protocol}://'
                                                                    f'{self.__server}/{self.__api_version}/'
                                                                    f'download/{self.__task}')
        if response.content_type == 'application/json':
            response_data: dict = await response.json()
            raise RuntimeError(str(response_data))
        else:
            with open(f'{output_path}/{response.content_disposition.parameters.get("filename")}', 'wb') as file:
                file.write(await response.read())
            return f'{output_path}/{response.content_disposition.parameters.get("filename")}'

    async def close_session(self):
        await self.__session.close()

    def __get_public_key(self) -> str:
        if not self.__public_keys:
            raise RuntimeError('Files limit reached or undefined public_key in config.ilovepdf_api')
        if type(self.__public_keys) == str:
            key: str = self.__public_keys
            self.__public_keys: None = None
            return key
        elif type(self.__public_keys) == list:
            try:
                return self.__public_keys.pop()
            except IndexError:
                raise RuntimeError('Files limit reached or undefined public_key in config.ilovepdf_api')
