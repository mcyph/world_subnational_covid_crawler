import os
import sys
import json
import datetime
import unicodedata
from os import makedirs
from os.path import dirname

from covid_19_au_grab.state_news_releases.act.ACTNews import ACTNews
from covid_19_au_grab.state_news_releases.nsw.NSWNews import NSWNews
from covid_19_au_grab.state_news_releases.nt.NTNews import NTNews
from covid_19_au_grab.state_news_releases.qld.QLDNews import QLDNews
from covid_19_au_grab.state_news_releases.sa.SANews import SANews
from covid_19_au_grab.state_news_releases.tas.TasNews import TasNews
from covid_19_au_grab.state_news_releases.vic.VicNews import VicNews
from covid_19_au_grab.state_news_releases.wa.WANews import WANews
from covid_19_au_grab.state_news_releases.constants import constant_to_name, schema_to_name
from covid_19_au_grab.get_package_dir import get_package_dir


UPDATE_VIC_POWERBI = False
UPDATE_ACT_POWERBI = False
UPDATE_WA_REGIONS = False
UPDATE_GRAPHS = True


if '--update-powerbi' in [i.strip() for i in sys.argv]:
    UPDATE_VIC_POWERBI = True
    UPDATE_ACT_POWERBI = True
    UPDATE_WA_REGIONS = True


def remove_control_characters(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C"
    )


class RevisionIDs:
    @staticmethod
    def get_latest_revision_id(time_format):
        x = 0
        revision_id = 1

        while True:
            if x > 1000:
                # This should never happen, but still..
                raise Exception()

            path = RevisionIDs.get_path_from_id(time_format, revision_id)
            if not os.path.exists(path):
                try:
                    makedirs(dirname(path))
                except OSError:
                    pass
                return revision_id

            revision_id += 1
            x += 1

    @staticmethod
    def get_path_from_id(time_format, revision_id, ext='tsv'):
        return (
            get_package_dir() / 'state_news_releases' / 'output' /
                f'{time_format}-{revision_id}.{ext}'
        )


TIME_FORMAT = datetime.datetime \
                      .now() \
                      .strftime('%Y_%m_%d')
LATEST_REVISION_ID = RevisionIDs.get_latest_revision_id(
    TIME_FORMAT
)


class Logger:
    def __init__(self, stream, ext='tsv'):
        revision_id = RevisionIDs.get_latest_revision_id(TIME_FORMAT)
        self.f = open(
            RevisionIDs.get_path_from_id(TIME_FORMAT, revision_id, ext),
            'w', encoding='utf-8', errors='replace'
        )
        self.stream = stream
        self.ext = ext

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
    status = {}
    stdout_logger = sys.stdout = Logger(sys.stdout, ext='stdout')
    stderr_logger = sys.stderr = Logger(sys.stdout, ext='stderr')

    # Run the Vic/ACT PowerBi grabbers as needed

    if UPDATE_VIC_POWERBI:
        from covid_19_au_grab.state_news_releases.vic.VicPowerBI import \
            VicPowerBI
        try:
            VicPowerBI().run_powerbi_grabber()
            status['vic_powerbi'] = ('OK', None)
        except:
            print("Error occurred using VicPowerBI!")
            import traceback
            traceback.print_exc()
            status['vic_powerbi'] = (
                'ERROR', traceback.format_exc()
            )

    if UPDATE_ACT_POWERBI:
        from covid_19_au_grab.state_news_releases.act.ACTPowerBI import \
            ACTPowerBI
        try:
            ACTPowerBI().run_powerbi_grabber()
            status['act_powerbi'] = ('OK', None)
        except:
            print("Error occurred using ACTPowerBI!")
            import traceback
            traceback.print_exc()
            status['act_powerbi'] = (
                'ERROR', traceback.format_exc()
            )

    if UPDATE_WA_REGIONS:
        from covid_19_au_grab.state_news_releases.wa.WARegions import \
            run_wa_regions
        try:
            run_wa_regions()
            status['wa_regions'] = ('OK', None)
        except:
            print("Error occurred using WA regions!")
            import traceback
            traceback.print_exc()
            status['wa_regions'] = (
                'ERROR', traceback.format_exc()
            )

    # Run all of the other grabbers
    news_insts = [
        ACTNews(),
        NSWNews(),
        NTNews(),
        QLDNews(),
        SANews(),
        TasNews(),
        VicNews(),
        WANews()
    ]

    data = {}
    for inst in news_insts:
        try:
            data[inst.STATE_NAME] = inst.get_data()
            status[inst.STATE_NAME] = (
                'OK', None
            )
        except:
            import traceback
            traceback.print_exc()
            status[inst.STATE_NAME] = (
                'ERROR', traceback.format_exc()
            )
    sys.stdout = stdout_logger.stream
    sys.stderr = stderr_logger.stream

    # Output basic status info to a .json info
    with open(
        RevisionIDs.get_path_from_id(
            TIME_FORMAT, LATEST_REVISION_ID,
            ext='json'
        ), 'w', encoding='utf-8'
    ) as f:
        f.write(json.dumps({
            'status': status
        }, indent=4))

    from pprint import pprint
    pprint(data)
    print()

    # Override stdout to point to both stdout and the output file
    logger = sys.stdout = Logger(sys.stdout)
    print('state_name\t'
          'schema\t'
          'datatype\t'
          'agerange\t'
          'region\t'
          'value\t'
          'date_updated\t'
          'source_url\t'
          'text_match')

    for state_name, datapoints in data.items():
        for datapoint in datapoints:
            try:
                text_match = repr(remove_control_characters(
                    str(datapoint.text_match).replace("\t", " ").replace('\n', ' ').replace('\r', ' ')
                ))
            except:
                print("ERROR:", datapoint)
                raise

            yyyy, mm, dd = datapoint.date_updated.split('_')
            backwards_date = f'{dd}/{mm}/{yyyy}'

            print(f'{state_name}\t'
                  f'{schema_to_name(datapoint.schema)[7:].lower()}\t'
                  f'{constant_to_name(datapoint.datatype)[3:].lower()}\t'
                  f'{datapoint.agerange}\t'
                  f'{datapoint.region}\t'
                  f'{datapoint.value}\t'
                  f'{backwards_date}\t'
                  f'{datapoint.source_url}\t'
                  f'{text_match}')
    # Reset stdout
    sys.stdout = logger.stream

    if UPDATE_GRAPHS:
        from covid_19_au_grab.output_graphs.output_graphs import output_graphs
        output_graphs()
