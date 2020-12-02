import threading
import multiprocessing
from queue import Queue

from covid_19_au_grab.state_news_releases.act.ACTNews import ACTNews
from covid_19_au_grab.state_news_releases.act.ACTPowerBIReader import ACTPowerBIReader

from covid_19_au_grab.state_news_releases.nsw.NSWNews import NSWNews
from covid_19_au_grab.state_news_releases.nsw.NSWJSONOpenData import NSWJSONOpenData
from covid_19_au_grab.state_news_releases.nsw.NSWJSONWebsiteData import NSWJSONWebsiteData

from covid_19_au_grab.state_news_releases.nt.NTNews import NTNews
from covid_19_au_grab.state_news_releases.qld.QLDNews import QLDNews

from covid_19_au_grab.state_news_releases.sa.SANews import SANews
from covid_19_au_grab.state_news_releases.sa.SARegionsReader import SARegionsReader
from covid_19_au_grab.state_news_releases.sa.SAJSONReader import SAJSONReader

from covid_19_au_grab.state_news_releases.tas.TasNews import TasNews
from covid_19_au_grab.state_news_releases.tas.TasFacebook import TasFacebook

from covid_19_au_grab.state_news_releases.vic.VicNews import VicNews
from covid_19_au_grab.state_news_releases.vic.VicPowerBIReader import VicPowerBIReader
from covid_19_au_grab.state_news_releases.vic.VicGoogleSheets import VicGoogleSheets
from covid_19_au_grab.state_news_releases.vic.VicCSV import VicCSV
from covid_19_au_grab.state_news_releases.vic.VicTableauNative import VicTableauNative

from covid_19_au_grab.state_news_releases.wa.WANews import WANews
from covid_19_au_grab.state_news_releases.wa.WADashReader import WADashReader

from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.datatypes.DataPoint import DataPoint, _DataPoint


class StateDataSources:
    def __init__(self):
        self._status = {}

    def iter_data_sources(self):
        processes = []
        all_source_ids = []
        #send_q = Queue()
        send_q = multiprocessing.Queue()

        # Run all of the other grabbers
        news_insts = [
            # We'll make it so crawlers with dashboards run
            # together with ones which don't when possible
            (NSWNews, NSWJSONOpenData, NSWJSONWebsiteData),
            (ACTNews, ACTPowerBIReader),
            (QLDNews,),
            (NTNews,),
            (SANews, SARegionsReader, SAJSONReader),
            (WANews, WADashReader),
            (TasNews, TasFacebook),
            (VicNews, VicPowerBIReader, VicGoogleSheets, VicCSV, VicTableauNative),
        ]

        for klass_set in news_insts:
            all_source_ids.extend([i.SOURCE_ID for i in klass_set])

            #process = threading.Thread(
            #    target=_get_datapoints, args=(klass_set, send_q)
            #)
            process = multiprocessing.Process(
                target=_get_datapoints, args=(klass_set, send_q)
            )

            print("START:", klass_set)
            process.start()
            processes.append(process)

        num_done = 0

        while num_done != len(processes):
            while True:
                try:
                    q_item = send_q.get(timeout=60 * 3)
                    break
                except:
                    for i in all_source_ids:
                        if i not in self._status:
                            print('NOT COMPLETED:', i)

            if q_item is None:
                num_done += 1
                continue

            source_id, source_url, source_description, new_datapoints, status_dict = q_item
            self._status[source_id] = status_dict

            if new_datapoints is not None:
                new_datapoints = [_DataPoint(*i) for i in new_datapoints]
                yield source_id, source_url, source_description, new_datapoints
                del new_datapoints

        for process in processes:
            try:
                process.join(timeout=10)
            except:
                import traceback
                traceback.print_exc()

    def get_status_dict(self):
        return self._status


def _get_datapoints(classes, send_q):
    print("GET DATAPOINTS:", classes, send_q)

    for i in classes:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        print("Getting using class:", i)

        inst = i()

        try:
            datapoints = inst.get_datapoints()

            print("Class done:", i)
            send_q.put((inst.SOURCE_ID,
                  inst.SOURCE_URL,
                  inst.SOURCE_DESCRIPTION,
                  datapoints, {
                'status': 'OK',
                'message': None,
            }))

            # Reduce memory usage!
            del datapoints

        except:
            print("Class done with exception:", i)
            import traceback
            traceback.print_exc()

            send_q.put((
                # WARNING WARNING: This will have trouble when the source ID is OVERRIDDEN!!!!! ================================================================

                inst.SOURCE_ID,
                  inst.SOURCE_URL,
                  inst.SOURCE_DESCRIPTION,
                  None, {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }))

    print("End of worker:", classes)
    send_q.put(None)


if __name__ == '__main__':
    for i in StateDataSources().iter_data_sources():
        print(i[:3])
