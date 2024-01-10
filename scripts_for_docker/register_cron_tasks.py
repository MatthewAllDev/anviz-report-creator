#!/usr/bin/env python

import os

if __name__ == '__main__':
    os.system('crontab -l > temp_cron')
    with open('/usr/src/app/docker_tasks', 'r', encoding='utf-8') as tasks_file:
        tasks: str = tasks_file.read()
    with open('temp_cron', 'a') as temp_file:
        temp_file.write(tasks)
    os.system('crontab temp_cron')
    os.remove('temp_cron')
