from anviz_report_creator.db.models import Record
from .report import Report
from .work_time_for_period import WorkTimeForPeriod


def first_in_last_out(report: Report):
    if len(report.records) == 0:
        return
    first_record: Record = report.records[0]
    user_name: str = ''
    for index, record in enumerate(report.records):
        record: Record
        if first_record.check_time.date() != record.check_time.date() or first_record.user_id != record.user_id:
            if record.check_type_id != 0 and not record.is_error_record:
                record.is_warning_record = True
                report.records[index].error_reason += 'Invalid status; '
            if report.records[index - 1].check_type_id != 1 and not report.records[index - 1].is_error_record:
                report.records[index - 1].is_warning_record = True
                report.records[index - 1].error_reason += 'Invalid status; '
            if report.records[index - 1] == first_record:
                report.records[index - 1].is_error_record = True
                report.records[index - 1].error_reason += 'Single record; '
                report.users_work_time_on_date[user_name].set(first_record.check_time.date(),
                                                              None,
                                                              is_error_record=True,
                                                              error_type='SR')
            first_record = record
            if report.records[index - 1].error_reason == 'Excess record; ':
                report.records[index - 1].is_warning_record = False
            report.records[index - 1].error_reason = \
                report.records[index - 1].error_reason.replace('Excess record; ', '')
        elif index != 0:
            record.is_warning_record = True
            record.error_reason += 'Excess record; '
        user_name: str = record.user.name.replace('\xa0', ' ')
        user_name: str = f'{user_name} ({record.user.id})'
        if not report.users_work_time_on_date.get(user_name):
            report.users_work_time_on_date[user_name] = WorkTimeForPeriod(report.periods, user_name)
        report.users_work_time_on_date[user_name].set(first_record.check_time.date(),
                                                      record.check_time - first_record.check_time)
    if report.records[len(report.records) - 1].error_reason == 'Excess record; ':
        report.records[len(report.records) - 1].is_warning_record = False
    report.records[len(report.records) - 1].error_reason = \
        report.records[len(report.records) - 1].error_reason.replace('Excess record; ', '')
