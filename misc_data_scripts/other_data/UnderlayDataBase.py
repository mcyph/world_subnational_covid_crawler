import json
from abc import ABC, abstractmethod
from misc_data_scripts.other_data import TimeSeriesSource


class UnderlayDataBase(ABC):
    def __init__(self, name, desc):
        self.time_series_source = TimeSeriesSource(name, desc)
        self.__processed = False

    @abstractmethod
    def process_data(self):
        pass

    def get_encoded_data(self, *args, **kw):
        if not len(list(self.time_series_source.keys())):
            self.process_data()
        return self.time_series_source.get_encoded(*args, **kw)

    def get_encoded_data_as_json(self, pretty_print=False, *args, **kw):
        if pretty_print:
            return json.dumps(self.get_encoded_data(*args, **kw),
                              indent=4)
        else:
            return json.dumps(self.get_encoded_data(*args, **kw),
                              separators=(',', ':'),
                              ensure_ascii=False)
