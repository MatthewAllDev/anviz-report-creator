from departments_desc import departments
from anviz_report_creator import ReportCreator
from custom_date import CustomDate
import shutil
import os

department_ids: list = list(departments.keys())
report_creator: ReportCreator = ReportCreator(department_ids, 'temp_excel', 'temp_pdf', True)
today: CustomDate = CustomDate()
if today.day < 15:
    start_date: CustomDate = today.dec(months=1).get_month_start_date()
    finish_date: CustomDate = today.dec(months=1).get_month_end_date()
else:
    start_date: CustomDate = today.get_month_start_date()
    finish_date: CustomDate = today.get_month_end_date()
report_creator.create_reports((start_date.upcast(), finish_date.upcast()))
for file in os.listdir('temp_pdf'):
    departament_id: int = int(file.split('-')[0])
    if not os.path.exists(f'{departments[departament_id].directory}/{start_date.strftime("%Y %B")}'):
        os.makedirs(f'{departments[departament_id].directory}/{start_date.strftime("%Y %B")}')
    shutil.move(f'temp_pdf/{file}', f'{departments[departament_id].directory}/{start_date.strftime("%Y %B")}/{file}')
shutil.rmtree('temp_excel')
shutil.rmtree('temp_pdf')
