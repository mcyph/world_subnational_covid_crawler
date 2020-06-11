from covid_19_au_grab.other_data.TimeSeriesSource import TimeSeriesSource


class UnderlayDataBase:
    def __init__(self, name, desc):
        self.time_series_source = TimeSeriesSource(name, desc)

