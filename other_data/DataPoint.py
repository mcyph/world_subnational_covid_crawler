from covid_19_au_grab.other_data.DateType import DateType


class DataPoint:
    def __init__(self, date, region_schema, region_parent, region_child, value):
        """

        """
        if isinstance(date, str):
            self.date = DateType.from_string(date)
        elif isinstance(date, DateType):
            self.date = date
        else:
            raise Exception(date)

        self.region_schema = region_schema
        self.region_parent = region_parent
        self.region_child = region_child

        assert isinstance(value, (int, float)), value
        self.value = value
