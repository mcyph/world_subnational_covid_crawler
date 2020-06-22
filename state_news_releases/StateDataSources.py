from covid_19_au_grab.state_news_releases.act.ACTNews import ACTNews
from covid_19_au_grab.state_news_releases.nsw.NSWNews import NSWNews
from covid_19_au_grab.state_news_releases.nt.NTNews import NTNews
from covid_19_au_grab.state_news_releases.qld.QLDNews import QLDNews
from covid_19_au_grab.state_news_releases.sa.SANews import SANews
from covid_19_au_grab.state_news_releases.tas.TasNews import TasNews
from covid_19_au_grab.state_news_releases.vic.VicNews import VicNews
from covid_19_au_grab.state_news_releases.wa.WANews import WANews
from covid_19_au_grab.datatypes.constants import SCHEMA_ADMIN_1, datatype_to_name, schema_to_name
from covid_19_au_grab.datatypes.DataPoint import DataPoint


class StateDataSources:
    def __init__(self):
        self._status = {}

    def iter_data_sources(self):
        # Run all of the other grabbers
        news_insts = [
            ACTNews,
            NSWNews,
            NTNews,
            QLDNews,
            SANews,
            TasNews,
            VicNews,
            WANews
        ]

        for klass in news_insts:
            inst = klass()

            try:
                datapoints = inst.get_data()

                new_datapoints = [
                    DataPoint(
                        region_schema=dp.region_schema,
                        region_parent=(
                            inst.SOURCE_ISO_3166_2
                            if dp.region_schema != SCHEMA_ADMIN_1
                            else 'AU'
                        ),
                        region_child=(
                            dp.region_child
                            if dp.region_schema != SCHEMA_ADMIN_1
                            else inst.SOURCE_ISO_3166_2
                        ),
                        date_updated=dp.date_updated,
                        datatype=dp.datatype,
                        agerange=dp.agerange,
                        value=dp.value,
                        source_url=dp.source_url,
                        text_match=dp.text_match
                    ) for dp in datapoints
                ]

                yield inst.SOURCE_ID, \
                      inst.SOURCE_URL, \
                      inst.SOURCE_DESCRIPTION, \
                      new_datapoints

                self._status[inst.SOURCE_ID] = {
                    'status': 'OK',
                    'message': None,
                }

            except:
                import traceback
                traceback.print_exc()

                self._status[inst.SOURCE_ID] = {
                    'status': 'ERROR',
                    'message': traceback.format_exc()
                }

    def get_status_dict(self):
        return self._status
