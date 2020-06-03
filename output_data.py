import sys
import json
import datetime

from covid_19_au_grab.db.RevisionIDs import RevisionIDs
from covid_19_au_grab.db.DataPointsDB import DataPointsDB
from covid_19_au_grab.overseas.OverseasDataSources import OverseasDataSources
from covid_19_au_grab.state_news_releases.StateDataSources import StateDataSources
from covid_19_au_grab.state_news_releases.InfrequentStateDataJobs import InfrequentStateDataJobs

from covid_19_au_grab.Logger import Logger


TIME_FORMAT = datetime.datetime \
                      .now() \
                      .strftime('%Y_%m_%d')
LATEST_REVISION_ID = RevisionIDs.get_latest_revision_id(
    TIME_FORMAT
)

RUN_INFREQUENT_JOBS = '--run-infrequent-jobs' in [i.strip() for i in sys.argv]


def run_infrequent_jobs():
    """
    Run infrequent tasks which require more resources
    Comment out any of these if they break!
    """
    isdj = InfrequentStateDataJobs()
    isdj.update_wa_regions()
    isdj.update_vic_powerbi()
    isdj.update_sa_regions()
    isdj.update_act_powerbi()
    return isdj.get_status()


def _rem_dupes(datapoints):
    """
    Remove dupes!
    """
    add_me = set()
    for datapoint in datapoints:
        if datapoint in add_me:
            continue
        add_me.add(datapoint)
    return list(add_me)


def output_overseas_data(dpdb):
    """
    Output from overseas data
    """
    ods = OverseasDataSources()
    for source_id, source_url, source_desc, datapoints in \
            ods.iter_data_sources():
        dpdb.extend(source_id, _rem_dupes(datapoints),
                    is_derived=False)
    return ods.get_status_dict()


def output_state_data(dpdb):
    """
    Output from state data
    """
    sds = StateDataSources()
    for source_id, source_url, source_desc, datapoints in \
            sds.iter_data_sources():
        dpdb.extend(source_id, _rem_dupes(datapoints),
                    is_derived=False)
    return sds.get_status_dict()


if __name__ == '__main__':
    status = {}

    # Output stdout/stderr to log files
    stdout_logger = sys.stdout = Logger(
        sys.stdout, ext='stdout'
    )
    stderr_logger = sys.stderr = Logger(
        sys.stderr, ext='stderr'
    )

    # Open the new output SQLite database
    revision_id = RevisionIDs.get_latest_revision_id(
        TIME_FORMAT
    )
    sqlite_path = RevisionIDs.get_path_from_id(
        TIME_FORMAT, revision_id, 'sqlite'
    )
    dpdb = DataPointsDB(sqlite_path)

    if RUN_INFREQUENT_JOBS:
        status.update(run_infrequent_jobs)

    status.update(output_state_data(dpdb))
    status.update(output_overseas_data(dpdb))

    dpdb.commit()
    dpdb.close()

    # Output basic status info to a .json info
    with open(
        RevisionIDs.get_path_from_id(
            TIME_FORMAT, LATEST_REVISION_ID, 'json'
        ), 'w', encoding='utf-8'
    ) as f:
        f.write(json.dumps({
            'status': status
        }, indent=4))
