from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    DT_STATUS_ACTIVE
)


def gaps_filled_in(datapoints):
    """
    When there are patient cases in open data, effectively we
    can assume there is updated data for every day for each
    region, it's just that there are only datapoints
    corresponding to when individual people were diagnosed
    """
    datapoints.sort(key=lambda i: i.date_updated)

    out = []
    all_dates = set()
    added_all_dates = {}
    current_date = None
    added_current_date = {}

    def process(current_date, added_current_date):
        for k, datapoint in added_all_dates.items():
            if k in added_current_date:
                continue

            # HACK: Many sources which don't provide active values
            # on a given day might imply active cases are down to 0.
            # Really should add separate logic, but until I figure
            # out exactly how this will work, would rather disallow
            # active values entirely!
            assert datapoint.datatype != DT_STATUS_ACTIVE

            out.append(DataPoint(
                statename=datapoint.statename,
                schema=datapoint.schema,
                datatype=datapoint.datatype,
                agerange=datapoint.agerange,
                region=datapoint.region,
                value=datapoint.value,
                date_updated=current_date,
                source_url=datapoint.source_url,
                text_match=datapoint.text_match
            ))

    for datapoint in datapoints:
        if current_date != datapoint.date_updated:
            if current_date is not None:
                process(current_date, added_current_date)
            current_date = datapoint.date_updated
            added_current_date = {}

        key = (
            datapoint.statename,
            datapoint.schema, datapoint.datatype,
            datapoint.region, datapoint.agerange
        )
        added_current_date[key] = datapoint
        added_all_dates[key] = datapoint
        all_dates.add(datapoint.date_updated)
        out.append(datapoint)

    process(current_date, added_current_date)
    return out
