import datetime
import math


class WorkTime:
    def __init__(self,
                 time: datetime.timedelta or None,
                 is_error_record: bool = False,
                 error_type: str = '',
                 is_holiday: bool = False):
        if time is None:
            time = datetime.timedelta(0)
        self.time:  datetime.timedelta = time
        self.is_error_record: bool = is_error_record
        self.error_type: str = error_type
        self.is_holiday: bool = is_holiday

    def __str__(self):
        if self.is_error_record:
            return self.error_type
        minutes: float = math.ceil(self.time.total_seconds() / 60)
        return f'{minutes // 60}:{minutes % 60 if minutes % 60 > 9 else f"0{minutes % 60}"}'

    def set(self, time: datetime.timedelta or None, is_error_record: bool = False, error_type: str = ''):
        if time is None:
            time = datetime.timedelta(0)
        self.time: datetime.timedelta = time
        self.is_error_record: bool = is_error_record
        self.error_type: str = error_type

