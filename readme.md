# Anviz report creator

## Installation

1. Install "pyodbc" according to the instructions: https://github.com/mkleehammer/pyodbc/wiki/Install
2. Clone the repo:
```sh 
git clone https://github.com/MatthewAllDev/anviz-report-creator
```
3. Install requirements:
```sh
pip install -r requirements.txt
```
4. If you want to use converting reports to PDF, get API keys: https://developer.ilovepdf.com/signup
5. Set the database connection settings in “config.json”, as well as the API keys from the previous step
6. [Use in console mode](#usage) or import into your project (see ["example" directory](example))

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