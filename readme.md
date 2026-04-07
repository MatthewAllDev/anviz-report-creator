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

**5. Set the database connection settings and API keys by running the configuration script:**
```sh
./init_config_script.py
```
This will interactively prompt for settings and update `config.json`.

**6. [Use in console mode](#usage) or import into your project (see ["example" directory](example))**


## Installation with Docker

**0. First depending on your operating system you need to install and setup docker. You can find out how to install it [here](https://docs.docker.com/engine/install/). And clone this project.**
```sh 
git clone https://github.com/MatthewAllDev/anviz-report-creator
```
**1. Go to project directory**

**2. (optional) If you want to use converting reports to PDF, get API keys: https://developer.ilovepdf.com/signup**

**3. Set the database connection settings and API keys by running the configuration script:**
```sh
./init_config_script.py
```
This will update `config.json` with your settings.

**4. (optional) If you don't want to use console mode, create your project based on ["example" directory](example)**

**5. (optional) If you want to run the application on a schedule, create a cron task using the command:**
```sh
python scripts_for_docker/create_cron_task.py
```
**6. Build and run with docker-compose:**
```sh
docker compose up --build
```
The application will run with cron by default. To run in interactive mode or with custom commands, you can modify `docker-compose.yml` or use `docker compose run anviz-app /bin/sh`.

**Note:** Since the project directory is mounted as a volume, you can edit files outside the container, and changes will be reflected inside. Configuration can be updated by running `./init_config_script.py` again.

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