import asyncio
import os
from .async_ilovepdf_api import API
from .async_ilovepdf_api import Settings as APISettings


class Convertor:
    def __init__(self, api_settings: APISettings, output_file_path: str = None):
        if output_file_path is not None:
            self.__output_file_path: str = output_file_path
        else:
            self.__output_file_path: str = 'output'
        os.makedirs(self.__output_file_path, exist_ok=True)
        self.__api = API('officepdf', api_settings)

    def convert(self, files: list or str):
        loop = asyncio.get_event_loop()
        a = loop.run_until_complete(self.__async_convert(files))
        return a

    async def __async_convert(self, files: list or str) -> str:
        await self.__api.create_task()
        tasks: list = []
        print('     Uploading files...')
        if type(files) == list:
            for file in files:
                tasks.append(self.__api.upload_file(file))
            await asyncio.gather(*tasks)
        else:
            await self.__api.upload_file(files)
        print('     Processing files...')
        await self.__api.process()
        print('     Downloading files...')
        file: str = await self.__api.download(self.__output_file_path)
        await self.__api.close_session()
        return file
