import datetime


def only_positive(number: int) -> int:
    return int(((number * number) ** (1 / 2) + number) / 2)


class CustomDate(datetime.date):
    def __new__(cls, year: int = None, month: int = None, day: int = None) -> 'CustomDate':
        today: datetime.date = datetime.date.today()
        if year is None:
            year = today.year
        if month is None:
            month = today.month
        if day is None:
            day = today.day
        return super().__new__(cls, year, month, day)

    def inc(self, years: int = 0, months: int = 0, days: int = 0) -> 'CustomDate':
        if years == 0 and months == 0 and days == 0:
            days = 1
        year: int = self.year + years + (self.month + months - 1) // 12
        month: int = (self.month + months) % 12 + int(not bool((self.month + months) % 12)) * 12
        day: int = self.day
        max_day: int = self.get_max_days_in_month(year, month)
        if day > max_day:
            day = max_day
        day += days
        while day > max_day:
            day -= max_day
            month += 1
            if month > 12:
                year += 1
                month = 1
            max_day: int = self.get_max_days_in_month(year, month)
        return type(self)(year, month, day)

    def dec(self, years: int = 0, months: int = 0, days: int = 0) -> 'CustomDate':
        if years == 0 and months == 0 and days == 0:
            days = 1
        year: int = self.year - years - (only_positive(months - self.month)) // 12 - int(
            not bool(only_positive(self.month - months)))
        month: int = self.month - months % 12 + int(not bool(only_positive(self.month - months % 12))) * 12
        day: int = self.day - days
        while day < 1:
            month -= 1
            if month < 1:
                year -= 1
                month = 1
            max_day: int = self.get_max_days_in_month(year, month)
            day += max_day
        return self.replace(year, month, day)

    def get_max_days_in_month(self, year: int = None, month: int = None) -> int:
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        max_day: int = 28 + (month + month // 8) % 2 + 2 % month + 2 * (1 // month)
        if month == 2 and self.is_year_leap(year):
            max_day += 1
        return max_day

    def is_year_leap(self, year: int = None) -> bool:
        if year is None:
            year = self.year
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    def get_year_start_date(self, year: int = None) -> 'CustomDate':
        if year is None:
            year = self.year
        return type(self)(year, 1, 1)

    def get_year_end_date(self, year: int = None) -> 'CustomDate':
        if year is None:
            year = self.year
        return type(self)(year, 12, 31)

    def get_month_start_date(self, year: int = None, month: int = None) -> 'CustomDate':
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        return type(self)(year, month, 1)

    def get_month_end_date(self, year: int = None, month: int = None) -> 'CustomDate':
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        return type(self)(year, month, self.get_max_days_in_month(year, month))

    def get_week_start_date(self, year: int = None, month: int = None, day: int = None) -> 'CustomDate':
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        date: CustomDate = type(self)(year, month, day)
        return date.dec(days=date.isoweekday() - 1)

    def get_week_end_date(self, year: int = None, month: int = None, day: int = None) -> 'CustomDate':
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        date: CustomDate = type(self)(year, month, day)
        return date.inc(days=7 - date.isoweekday())

    def upcast(self) -> datetime.date:
        return datetime.date(self.year, self.month, self.day)
