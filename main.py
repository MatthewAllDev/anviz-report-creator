from anviz_report_creator import ReportCreator
import argparse
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start_date', help='Start date for report')
    parser.add_argument('finish_date', help='Finish date for report')
    parser.add_argument('-efd', '--excel_files_directory', type=str, default='output_excel',
                        help='Directory for excel files')
    parser.add_argument('-pfd', '--pdf_files_directory', type=str, default='output_pdf',
                        help='Directory for pdf files')
    parser.add_argument('-c', '--convert_to_pdf',
                        action='store_true', help='Convert reports to pdf flag')
    args: argparse.Namespace = parser.parse_args()
    date_range: tuple = (datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date(),
                         datetime.datetime.strptime(args.finish_date, '%Y-%m-%d').date())
    if date_range[1] < date_range[0]:
        raise AttributeError('start_date must be < finish_date')
    creator: ReportCreator = ReportCreator(directory_path_excel_files=args.excel_files_directory,
                                           directory_path_pdf_files=args.pdf_files_directory,
                                           convert_to_pdf=args.convert_to_pdf, departments_id=None)
    creator.create_reports(date_range)
