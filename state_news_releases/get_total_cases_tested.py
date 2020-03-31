import unicodedata

from covid_19_au_grab.state_news_releases.ACTNews import ACTNews
from covid_19_au_grab.state_news_releases.NSWNews import NSWNews
#from covid_19_au_grab.state_news_releases.NTNews import NTNews
from covid_19_au_grab.state_news_releases.QLDNews import QLDNews
from covid_19_au_grab.state_news_releases.SANews import SANews
from covid_19_au_grab.state_news_releases.TasNews import TasNews
from covid_19_au_grab.state_news_releases.VicNews import VicNews
from covid_19_au_grab.state_news_releases.WANews import WANews
from covid_19_au_grab.state_news_releases.constants import constant_to_name


def remove_control_characters(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C"
    )


if __name__ == '__main__':
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

    print('state_name\tdatatype\tvalue\tdate_updated\tsource_url\ttext_match')
    for state_name, datapoints in data.items():
        for datapoint in datapoints:
            text_match = repr(remove_control_characters(
                str(datapoint.text_match).replace("\t", " ").replace('\n', ' ').replace('\r', ' ')
            ))
            print(f'{state_name}\t'
                  f'{constant_to_name(datapoint.datatype)}\t'
                  f'{datapoint.value}\t'
                  f'{datapoint.date_updated}\t'
                  f'{datapoint.source_url}\t'
                  f'{text_match}')

