import os
import zipfile
from .progress_bar import ProgressBar
from .db.models import Departament
from .excel_to_pdf_convertor import Convertor
from .report_processor import Report, algorithms
from .settings import Settings
from .db import connection


class ReportCreator:
    def __init__(self, departments_id: list or int = None,
                 directory_path_excel_files: str = 'output_excel',
                 directory_path_pdf_files: str = 'output_pdf',
                 convert_to_pdf: bool = False,
                 config_file_path: str = 'config.json'):
        self.settings: Settings = Settings(config_file_path)
        connection.init(self.settings.db)
        self.departments: list = []
        if departments_id is None:
            self.departments: list = list(Departament.get_all())
        elif type(departments_id) == int:
            self.departments.append(Departament.get(departments_id))
        elif type(departments_id) == list:
            for department_id in departments_id:
                self.departments.append(Departament.get(department_id))
        else:
            raise RuntimeError('departments_id must be list, int or None')
        self.directory_path_excel_files: str = directory_path_excel_files
        self.directory_path_pdf_files: str = directory_path_pdf_files
        self.convert_to_pdf: bool = convert_to_pdf

    def create_reports(self, date_range: tuple):
        files: list = []
        print('Creating excel reports...\n')
        progress: ProgressBar = ProgressBar(len(self.departments))
        for index, department in enumerate(self.departments):
            progress.show()
            department: Departament
            report: Report = Report(departament_id=department.id,
                                    date_range=date_range,
                                    algorithm=algorithms.first_in_last_out)
            if len(report.records) == 0:
                progress.inc()
                continue
            files.append(report.save_records_log(self.directory_path_excel_files))
            files.append(report.save_work_time_report(self.directory_path_excel_files))
            progress.inc()
        progress.show()
        print()
        if self.convert_to_pdf:
            print('Converting files...')
            convertor = Convertor(self.settings.convertor, self.directory_path_pdf_files)
            file: str = convertor.convert(files)
            if file[-3:] == 'zip':
                print('\nExtract files...')
                with zipfile.ZipFile(file, 'r') as zip_file:
                    zip_file.extractall(self.directory_path_pdf_files)
                os.remove(file)
        print('Complete...')
