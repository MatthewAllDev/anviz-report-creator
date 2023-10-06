import os
import re
import pandas
from anviz_report_creator.db.models import Record, Departament, User
from anviz_report_creator.excel_processor import ExcelProcessor
from anviz_report_creator.excel_processor.row import Row
from .work_time_for_period import WorkTimeForPeriod


class Report:
    def __init__(self, date_range: tuple, algorithm, departament_id: int = None, user_ids: list = None):
        self.users_work_time_on_date: dict = {}
        self.__date_range: tuple = date_range
        self.__departament: Departament or None = None
        if departament_id is not None and user_ids is not None:
            raise AttributeError('Only departament_id or user_ids must be defined.')
        elif departament_id is None and user_ids is None:
            raise AttributeError('Departament_id or user_ids must be defined.')
        elif departament_id is not None:
            self.__user_ids: list = User.get_ids(departament_id=departament_id)
            self.__departament: Departament = Departament.get(departament_id)
        elif user_ids is not None:
            self.__user_ids: list = user_ids
        self.__departament_id: int = departament_id
        self.records: list = list(Record.get(user_ids=self.__user_ids, date_range=self.__date_range))
        self.periods: tuple = tuple(map(lambda period: period.date(),
                                        pandas.date_range(self.__date_range[0], self.__date_range[1])))
        algorithm(self)

    def save_records_log(self, directory_path: str = '') -> str:
        os.makedirs(directory_path, exist_ok=True)
        if len(directory_path) > 0 and directory_path[-1] not in ('/', '\\'):
            directory_path += '/'
        excel = ExcelProcessor()
        excel.set_fit_to_width()
        excel.set_margins(0.1, 0.1, 0.5)
        excel.add_row('Record ID',
                      'User name',
                      'Check time',
                      'Check type',
                      'Device',
                      'Error reason').font_style(bold=True).set_borders()
        for record in self.records:
            record: Record
            row: Row = excel.add_row(*tuple(record)).set_borders()
            if record.is_error_record:
                row.paint(color='E6B9B8')
            elif record.is_warning_record:
                row.paint(color='FFFFCC')
        excel.set_optimal_column_widths()
        if self.__departament is None:
            report_files: filter = filter(lambda report_file: re.fullmatch(r'Records log\s\(\d+\).*', report_file),
                                          os.listdir(directory_path if directory_path != '' else None))
            index: int = max(map(lambda report_file: int(re.search(r'\d+', report_file).group()), report_files)) + 1
            file_name: str = f'Records log ({index})'
        else:
            file_name: str = f'{self.__departament.id}-Records log {self.__departament.name}'
        return excel.save(f'{directory_path}{file_name} ({self.__date_range[0]} '
                          f'to {self.__date_range[1]}).xlsx')

    def save_work_time_report(self, directory_path: str = '') -> str:
        os.makedirs(directory_path, exist_ok=True)
        if len(directory_path) > 0 and directory_path[-1] not in ('/', '\\'):
            directory_path += '/'
        excel = ExcelProcessor()
        excel.set_orientation('landscape')
        excel.set_fit_to_width()
        excel.set_margins(0.1, 0.1, 0.5)
        row: Row = excel.add_row('User name',
                                 *map(lambda per: {'value': per.strftime('%d\n%m'),
                                                   'color': 'E6E6E6' if WorkTimeForPeriod.is_holiday(per) else None},
                                      self.periods), 'Amount')
        row.font_style(bold=True).set_borders().set_wrap_text()
        for user, work_time_on_dates in self.users_work_time_on_date.items():
            excel.add_row(*work_time_on_dates.to_epf()).set_borders()
        excel.set_optimal_column_widths()
        if self.__departament is None:
            report_files: filter = filter(lambda report_file: re.fullmatch(r'Work time report\s\(\d+\).*', report_file),
                                          os.listdir(directory_path if directory_path != '' else None))
            index: int = max(map(lambda report_file: int(re.search(r'\d+', report_file).group()), report_files)) + 1
            file_name: str = f'Work time report ({index})'
        else:
            file_name: str = f'{self.__departament.id}-Work time report {self.__departament.name}'
        return excel.save(f'{directory_path}{file_name} ({self.__date_range[0]} '
                          f'to {self.__date_range[1]}).xlsx')
