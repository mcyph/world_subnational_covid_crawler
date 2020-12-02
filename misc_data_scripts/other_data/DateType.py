class DateType:
    def __init__(self, year, month=None, day=None):
        """
        A date (without time) with year/month/day,
        with the month or day being optional.

        The year is first before months and days
        to allow for binary sorting.
        """
        self.year = int(year)
        self.month = month if month is None else int(month)
        self.day = day if day is None else int(day)

    @staticmethod
    def from_string(s):
        """
        Unserialize from a "YYYY((_MM)_DD)"-format string
        """
        if len(s) == 4:
            return DateType(int(s))
        elif len(s) == 7:
            return DateType(int(s[:4]), int(s[5:7]))
        elif len(s) == 10:
            return DateType(int(s[:4]), int(s[5:7], int(s[8:10])))
        else:
            raise Exception()

    def to_slash_format(self):
        """
        Output date in format ((DD/)MM/)YYYY
        """
        if self.year and self.month and self.day:
            return '%02d/%02d/%04d' % (self.day, self.month, self.year)
        elif self.year and self.month:
            return '%02d/%04d' % (self.month, self.year)
        elif self.year:
            return '%04d' % (self.year)
        else:
            raise Exception()

    def __str__(self):
        """
        Output date in format YYYY((_MM)_DD)
        """
        if self.year and self.month and self.day:
            return '%04d_%02d_%02d' % (self.year, self.month, self.day)
        elif self.year and self.month:
            return '%04d_%02d' % (self.year, self.month)
        elif self.year:
            return '%04d' % (self.year)
        else:
            raise Exception()
