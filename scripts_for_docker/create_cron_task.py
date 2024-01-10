#!/usr/bin/env python

import pathlib

if __name__ == '__main__':
    docker_tasks_file_path: pathlib.Path = pathlib.Path(pathlib.Path(__file__).parent.parent, 'cron_tasks')
    print(docker_tasks_file_path)
    schedule: str = input('Enter the task execution schedule in cron format\
    (by default, the first day of each month is 00:00 = 0 0 1 * *): ').strip()
    if schedule == "":
        schedule = "0 0 1 * *"
    schedule = '\t'.join(schedule.split(' '))
    file_name: str = input('Enter the name of the python file to run from the "/usr/src/app" directory,\
    without the ".py" extension (by default, "start"):').strip()
    if file_name == '':
        file_name = 'start'
    with open(docker_tasks_file_path, 'w', encoding='utf-8') as file:
        file.write(f'{schedule}\tcd /usr/src/app && python {file_name}.py\n')
