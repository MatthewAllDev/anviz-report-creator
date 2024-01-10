# Anviz report creator

## Installation

**1. Install "pyodbc" according to the instructions: https://github.com/mkleehammer/pyodbc/wiki/Install**

**2. Clone the repo:**
```sh 
git clone https://github.com/MatthewAllDev/anviz-report-creator
```
**3. Install requirements:**
```sh
pip install -r requirements.txt
```
**4. (optional) If you want to use converting reports to PDF, get API keys: https://developer.ilovepdf.com/signup**

**5. Set the database connection settings in “config.json”, as well as the API keys from the previous step**

**6. [Use in console mode](#usage) or import into your project (see ["example" directory](example))**


## Installation with Docker

**0. First depending on your operating system you need to install and setup docker. You can find out how to install it [here](https://docs.docker.com/engine/install/). And clone this project.**
```sh 
git clone https://github.com/MatthewAllDev/anviz-report-creator
```
**1. Go to project directory**

**2. (optional) If you want to use converting reports to PDF, get API keys: https://developer.ilovepdf.com/signup**

**3. Set the database connection settings in “config.json”, as well as the API keys from the previous step.**

**4. (optional) If you don't want to use console mode, create your project based on ["example" directory](example)**

**5. (optional) If you want to run the application on a schedule, create a cron task using the command:**
```sh
python scripts_for_docker/create_cron_task.py
```
**6. Build docker image**
```sh
docker build -t anviz-rc .
```
**7. Next you can create and run docker container**

a) If you want to use this with cron:
```sh
docker run -dt -v "{FULL_PATH_TO_HOST_DIR}:/home/app/output" --name anviz-rc anviz-rc
```
b) If you want to run your application:
```sh
docker run -it -v "{FULL_PATH_TO_HOST_DIR}:/home/app/output" --name anviz-rc anviz-rc {APP_CMD}
```
APP_CMD - is the command to run your app

c) If you want to use console mode:
```sh
docker run -it -v "{FULL_PATH_TO_HOST_DIR}:/home/app/output" --name anviz-rc anviz-rc /bin/sh
```
You can run app with the command:
```sh
python /usr/src/app/main.py {arguments} 
```

## Usage

```sh
main.py [-h] [-efd EXCEL_FILES_DIRECTORY] [-pfd PDF_FILES_DIRECTORY] [-c] start_date finish_date
```

#### positional arguments:

&emsp;**start_date**&nbsp; -  *Start date for report*\
&emsp;**finish_date** - *Finish date for report*

#### options:

&emsp;**-h, --help** - *Show help message and exit*\
&emsp;**-efd, --excel_files_directory** - *Directory for excel files*\
&emsp;**-pfd, --pdf_files_directory** - *Directory for pdf files*\
&emsp;**-c, --convert_to_pdf** - *Convert reports to pdf flag*