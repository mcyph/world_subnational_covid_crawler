import os
import sys
import datetime
import unicodedata
from os import makedirs
from os.path import dirname

from covid_19_au_grab.state_news_releases.ACTNews import ACTNews
from covid_19_au_grab.state_news_releases.NSWNews import NSWNews
#from covid_19_au_grab.state_news_releases.NTNews import NTNews
from covid_19_au_grab.state_news_releases.QLDNews import QLDNews
from covid_19_au_grab.state_news_releases.SANews import SANews
from covid_19_au_grab.state_news_releases.TasNews import TasNews
from covid_19_au_grab.state_news_releases.VicNews import VicNews
from covid_19_au_grab.state_news_releases.WANews import WANews
from covid_19_au_grab.state_news_releases.constants import constant_to_name


UPDATE_VIC_POWERBI = False


def remove_control_characters(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C"
    )


class Logger:
    def __init__(self, stream):
        time_format = datetime.datetime \
                              .now() \
                              .strftime('%Y_%m_%d')

        revision_id = self.get_latest_revision_id(time_format)
        self.f = open(
            self.get_path_from_id(time_format, revision_id),
            'w', encoding='utf-8', errors='replace'
        )
        self.stream = stream

    def get_latest_revision_id(self, time_format):
        x = 0
        revision_id = 1

        while True:
            if x > 1000:
                # This should never happen, but still..
                raise Exception()

            path = self.get_path_from_id(time_format, revision_id)
            if not os.path.exists(path):
                try:
                    makedirs(dirname(path))
                except OSError:
                    pass
                return revision_id

            revision_id += 1
            x += 1

    def get_path_from_id(self, time_format, revision_id):
        return os.path.expanduser(
            f'~/dev/covid_19_au_grab/state_news_releases/output/'
            f'{time_format}-{revision_id}.tsv'
        )

    def __del__(self):
        if hasattr(self, 'f'):
            self.f.close()

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        self.f.write(data)
        self.f.flush()

    def flush(self):
        self.stream.flush()
        self.f.flush()


if __name__ == '__main__':
    from covid_19_au_grab.vic_powerbi_grabber.vic_powerbi_grabber import grab

    if UPDATE_VIC_POWERBI:
        try:
            grab()
        except:
            print("Error occurred using VicPowerBI!")
            import traceback
            traceback.print_exc()

    news_insts = [
        ACTNews(),
        NSWNews(),
        #NTNews(),
        QLDNews(),
        SANews(),
        TasNews(),
        VicNews(),
        WANews()
    ]

    data = {}
    for inst in news_insts:
        data[inst.STATE_NAME] = inst.get_data()

    from pprint import pprint
    pprint(data)
    print()

    sys.stdout = Logger(sys.stdout)

    print('state_name\tdatatype\tname\tvalue\tdate_updated\tsource_url\ttext_match')
    for state_name, datapoints in data.items():
        for datapoint in datapoints:
            text_match = repr(remove_control_characters(
                str(datapoint.text_match).replace("\t", " ").replace('\n', ' ').replace('\r', ' ')
            ))
            yyyy, mm, dd = datapoint.date_updated.split('_')
            backwards_date = f'{dd}/{mm}/{yyyy}'

            print(f'{state_name}\t'
                  f'{constant_to_name(datapoint.datatype)}\t'
                  f'{datapoint.name}\t'
                  f'{datapoint.value}\t'
                  f'{backwards_date}\t'
                  f'{datapoint.source_url}\t'
                  f'{text_match}')

