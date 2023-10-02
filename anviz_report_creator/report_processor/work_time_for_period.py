import datetime

from .work_time import WorkTime


class WorkTimeForPeriod:
    def __init__(self, periods: tuple, user_name: str):
        self.periods: dict = {}
        self.user_name: str = user_name
        for period in periods:
            self.periods[period] = WorkTime(None,
                                            is_error_record=True,
                                            error_type='NE',
                                            is_holiday=True if self.is_holiday(period) else False)

    def set(self,
            period: datetime.date,
            time: datetime.timedelta or None,
            is_error_record: bool = False,
            error_type: str = ''):
        if not self.periods.get(period):
            raise KeyError('The period is not defined when the object is created')
        self.periods[period].set(time, is_error_record, error_type)

    def to_epf(self) -> tuple:
        """
        Convert WorkTimeForPeriod object to excel processor format tuple.
        """
        elements: list = []
        amount: WorkTime = WorkTime(datetime.timedelta(0))
        for period in self.periods.values():
            period: WorkTime
            color: str = 'FFFFFF'
            if period.is_holiday:
                if period.time == datetime.timedelta(0):
                    color = 'E6E6E6'
                else:
                    color = 'FFFF66'
            elif period.is_error_record:
                color = 'FF0000'
            amount.set(amount.time + period.time)
            elements.append({'value': str(period), 'color': color, 'font': None})
        return self.user_name, *elements, {'value': str(amount), 'color': 'E6E6E6', 'font': {'bold': True}}

    @staticmethod
    def is_holiday(day: datetime.date) -> bool:
        if day.isoweekday() > 5:
            return True
        else:
            return False
