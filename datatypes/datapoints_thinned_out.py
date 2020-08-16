from datetime import datetime, timedelta
from covid_19_au_grab.datatypes.constants import DT_NEW, DT_SOURCE_COMMUNITY, \
    DT_SOURCE_INTERSTATE, DT_SOURCE_CRUISE_SHIP, DT_SOURCE_DOMESTIC, \
    DT_SOURCE_CONFIRMED, DT_SOURCE_OVERSEAS, DT_SOURCE_UNDER_INVESTIGATION


def datapoints_thinned_out(datapoints):
    datapoints.sort(key=lambda i: (
        i.datatype,
        i.agerange,
        i.region_child,
        i.region_parent,
        i.region_schema,
        i.date_updated,
    ))

    out = []
    item = []
    last_unique_key = None

    def extend(item, unique_key):
        if unique_key[1] or unique_key[0] in (
            DT_NEW,
            DT_SOURCE_OVERSEAS,
            DT_SOURCE_UNDER_INVESTIGATION,
            DT_SOURCE_CONFIRMED,
            DT_SOURCE_DOMESTIC,
            DT_SOURCE_CRUISE_SHIP,
            DT_SOURCE_INTERSTATE,
            DT_SOURCE_COMMUNITY
        ):
            # Don't thin out if there's an agegroup
            # specified or the graphs might be affected
            out.extend(item)
        else:
            out.extend(_datapoints_thinned_out(item))

    for i in datapoints:
        unique_key = (
            i.datatype,
            i.agerange,
            i.region_child,
            i.region_parent,
            i.region_schema,
        )
        if last_unique_key != unique_key and item:
            extend(item, last_unique_key)
            item = []

        item.append(i)
        last_unique_key = unique_key

    if item:
        extend(item, last_unique_key)

    return sorted(
        out,
        key=lambda i: i.date_updated,
        reverse=True
    )


def _datapoints_thinned_out(datapoints):
    # Make sure in descending order
    # (so that older datapoints are first!)
    datapoints = sorted(datapoints,
                        key=lambda i: i.date_updated,
                        reverse=True)

    def _diff_from_today(date):
        today = datetime.today()
        date = datetime.strptime(date, '%Y_%m_%d')
        return abs((today - date).days)

    def _date_diff(date1, date2):
        date1 = datetime.strptime(date1, '%Y_%m_%d')
        date2 = datetime.strptime(date2, '%Y_%m_%d')

        return abs((
            date1 - date2
            if date2 > date2
            else date1 - date2
        ).days)

    def _get_dayskip(date):
        dft = _diff_from_today(date)

        if dft > (7*20):
            # > 20 weeks: 1 in 14 datapoints
            return 14
        elif dft > (7*18):
            # > 18 weeks: 1 in 7 datapoints
            return 6
        elif dft > (7*15):
            # > 15 weeks: 1 in 6 datapoints
            return 5
        elif dft > (7*12):
            # > 12 weeks: 1 in 5 datapoints
            return 4
        elif dft > (7*9):
            # > 9 weeks: 1 in 4 datapoints
            return 3
        elif dft > (7*6):
            # > 6 weeks: 1 in 3 datapoints
            return 2
        elif dft > (7*3):
            # > 3 weeks: 1 in 2 datapoints
            return 1
        else:
            # <= 3 weeks: don't skip
            return 0

    # datapoints is assumed to be sorted in descending order
    # (so newest datapoints come first)
    r = []
    cur_dayskip = None
    cur_date = None

    for datapoint in datapoints:
        if (
            cur_dayskip is not None and
            _date_diff(cur_date, datapoint.date_updated) <= cur_dayskip
        ):
            continue

        cur_dayskip = _get_dayskip(datapoint.date_updated)
        cur_date = datapoint.date_updated
        r.append(datapoint)

    return r
