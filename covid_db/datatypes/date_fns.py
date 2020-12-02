import datetime


def to_slash_format(d):
    yyyy, mm, dd = d.split('_')
    return f'{dd}/{mm}/{yyyy}'


def reverse_sort(d):
    yyyy, mm, dd = d.split('_')
    return f'{9999-yyyy}/{99-mm}/{99-dd}'


def to_datetime(d):
    return datetime.datetime.strptime(d, '%Y_%m_%d')


def from_datetime(d):
    return d.strftime('%Y_%m_%d')


def apply_timedelta(d, days=0, seconds=0, microseconds=0,
                    milliseconds=0, minutes=0, hours=0, weeks=0):

    td = datetime.timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks
    )
    d = datetime.datetime.strptime(d, '%Y_%m_%d') + td
    return d.strftime('%Y_%m_%d')
