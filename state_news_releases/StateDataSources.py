import multiprocessing

from covid_19_au_grab.state_news_releases.act.ACTNews import ACTNews
from covid_19_au_grab.state_news_releases.nsw.NSWNews import NSWNews
from covid_19_au_grab.state_news_releases.nt.NTNews import NTNews
from covid_19_au_grab.state_news_releases.qld.QLDNews import QLDNews
from covid_19_au_grab.state_news_releases.sa.SANews import SANews
from covid_19_au_grab.state_news_releases.tas.TasNews import TasNews
from covid_19_au_grab.state_news_releases.vic.VicNews import VicNews
from covid_19_au_grab.state_news_releases.wa.WANews import WANews
from covid_19_au_grab.datatypes.constants import SCHEMA_ADMIN_1, datatype_to_name, schema_to_name
from covid_19_au_grab.datatypes.DataPoint import DataPoint, _DataPoint


class StateDataSources:
    def __init__(self):
        self._status = {}

    def iter_data_sources(self):
        processes = []
        send_q = multiprocessing.Queue()

        # Run all of the other grabbers
        news_insts = [
            # We'll make it so crawlers with dashboards run
            # together with ones which don't when possible
            (NSWNews, ACTNews),
            (QLDNews, SANews),
            (VicNews, TasNews),
            (NTNews, WANews),
        ]

        for klass_set in news_insts:
            process = multiprocessing.Process(
                target=_get_datapoints, args=(klass_set, send_q)
            )
            print("START:", klass_set)
            process.start()
            processes.append(process)

        num_done = 0

        while num_done != len(processes):
            q_item = send_q.get()
            if q_item is None:
                num_done += 1
                continue

            source_id, source_url, source_description, new_datapoints, status_dict = q_item
            self._status[source_id] = status_dict

            if new_datapoints is not None:
                new_datapoints = [_DataPoint(*i) for i in new_datapoints]
                yield source_id, source_url, source_description, new_datapoints

        for process in processes:
            process.join()

    def get_status_dict(self):
        return self._status


def _get_datapoints(classes, send_q):
    print("GET DATAPOINTS:", classes, send_q)

    for i in classes:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        print("Getting using class:", i)

        inst = i()

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

            send_q.put((inst.SOURCE_ID,
                  inst.SOURCE_URL,
                  inst.SOURCE_DESCRIPTION,
                  [tuple(i) for i in new_datapoints], {
                'status': 'OK',
                'message': None,
            }))

        except:
            import traceback
            traceback.print_exc()

            send_q.put((inst.SOURCE_ID,
                  inst.SOURCE_URL,
                  inst.SOURCE_DESCRIPTION,
                  None, {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }))

    send_q.put(None)


if __name__ == '__main__':
    for i in StateDataSources().iter_data_sources():
        print(i[:3])
