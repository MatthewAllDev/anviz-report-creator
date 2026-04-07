#!/usr/bin/env python

import os
from pathlib import Path

if __name__ == '__main__':
    script_dir = Path(__file__).resolve().parent.parent
    cron_tasks_path = script_dir / 'cron_tasks'
    if not cron_tasks_path.exists():
        print(f'Skipping cron registration because {cron_tasks_path} does not exist.')
    else:
        os.system('crontab -l > temp_cron')
        with open(cron_tasks_path, 'r', encoding='utf-8') as tasks_file:
            tasks: str = tasks_file.read()
        with open('temp_cron', 'a') as temp_file:
            temp_file.write(tasks)
        os.system('crontab temp_cron')
        os.remove('temp_cron')
