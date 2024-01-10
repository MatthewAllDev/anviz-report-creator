FROM alpine:3.19
RUN apk add python3 python3-dev g++ unixodbc-dev curl
# openrc
RUN apk add py3-pip
RUN python -m pip install --user pyodbc --break-system-packages
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
RUN pip3 install -r /usr/src/app/requirements.txt --break-system-packages
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.5.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql17_17.10.5.1-1_amd64.apk
RUN rm msodbcsql17_17.10.5.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk
RUN rm mssql-tools_17.10.1.1-1_amd64.apk
RUN cat /etc/odbcinst.ini > /etc/odbc.ini
RUN chmod a+x /usr/src/app/scripts_for_docker/init_config_script.py
RUN ln -s /usr/src/app/scripts_for_docker/init_config_script.py /usr/bin/configurate
RUN chmod a+x /usr/src/app/scripts_for_docker/create_cron_task.py
RUN ln -s /usr/src/app/scripts_for_docker/create_cron_task.py /usr/bin/create_task
RUN chmod a+x /usr/src/app/scripts_for_docker/register_cron_tasks.py
RUN /usr/src/app/scripts_for_docker/register_cron_tasks.py
RUN apk del curl
RUN apk cache clean
RUN mkdir -p /home/app/output
RUN touch /home/app/output/cron.log
CMD ["crond", "-f", "-L", "/home/app/output/cron.log"]
ENV SHELL /bin/sh