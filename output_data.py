import sys
import json
import datetime
from git import Repo

from covid_19_au_grab.Logger import Logger
from covid_19_au_grab.get_package_dir import \
    get_output_dir, get_global_subnational_covid_data_dir
from covid_19_au_grab.overseas.OverseasDataSources import OverseasDataSources
from covid_19_au_grab.state_news_releases.StateDataSources import StateDataSources
from covid_19_au_grab.state_news_releases.InfrequentStateDataJobs import InfrequentStateDataJobs

from covid_19_au_grab.db.RevisionIDs import RevisionIDs
from covid_19_au_grab.db.DerivedData import DerivedData
from covid_19_au_grab.db.DataPointsDB import DataPointsDB
from covid_19_au_grab.db.SQLiteDataRevision import SQLiteDataRevision
from covid_19_au_grab.db.SQLiteDataRevisions import SQLiteDataRevisions


OUTPUT_DIR = get_output_dir() / 'output'
TIME_FORMAT = datetime.datetime.now().strftime('%Y_%m_%d')
LATEST_REVISION_ID = RevisionIDs.get_latest_revision_id(TIME_FORMAT)
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
    for source_id, source_url, source_desc, datapoints in ods.iter_data_sources():
        dpdb.extend(source_id, _rem_dupes(datapoints), is_derived=False)
    return ods.get_status_dict()


def output_state_data(dpdb):
    """
    Output from state data
    """
    sds = StateDataSources()
    for source_id, source_url, source_desc, datapoints in sds.iter_data_sources():
        dpdb.extend(source_id, _rem_dupes(datapoints), is_derived=False)
    return sds.get_status_dict()


if __name__ == '__main__':
    status = {}

    # Output stdout/stderr to log files
    stdout_logger = sys.stdout = Logger(sys.stdout, ext='stdout')
    stderr_logger = sys.stderr = Logger(sys.stderr, ext='stderr')

    # Open the new output SQLite database
    sqlite_path = RevisionIDs.get_path_from_id(
        TIME_FORMAT, LATEST_REVISION_ID, 'sqlite'
    )
    dpdb = DataPointsDB(sqlite_path)

    if RUN_INFREQUENT_JOBS:
        # Run infrequent jobs that need Selenium or other
        # high-processing tasks only a few times a day tops
        status.update(run_infrequent_jobs())

    # Output both state and overseas data from crawlers
    status.update(output_state_data(dpdb))
    status.update(output_overseas_data(dpdb))

    # If any of them failed, copy them across from the previous revision.
    # Note the previous revision might have failed too, but should have
    # copied the values from the previous revision before that, etc
    # (assuming the crawler worked in the past)
    migrate_source_ids = []
    for status_key, status_dict in status.items():
        if status_dict['status'] == 'ERROR':
            print("ERROR OCCURRED, reverting to previous source ID data:", status_key)
            migrate_source_ids.append(status_key)

    revisions = SQLiteDataRevisions()
    rev_date, rev_subid, dt = revisions.get_revisions()[0]
    prev_revision_path = revisions.get_revision_path(rev_date, rev_subid)
    dpdb.migrate_source_ids(prev_revision_path, migrate_source_ids)

    # Derive "new cases" from "total cases" when
    # they aren't explicitly specified, etc
    DerivedData(dpdb).add_derived()

    # Commit and close the DB
    dpdb.commit()
    dpdb.close()

    # Output basic status info to a .json info
    # This also signifies to the web
    # interface that the import went OK
    status_json_path = RevisionIDs.get_path_from_id(
        TIME_FORMAT, LATEST_REVISION_ID, 'json'
    )
    with open(status_json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'status': status}, indent=4))

    # Update the csv output
    sqlite_data_revision = SQLiteDataRevision(TIME_FORMAT, LATEST_REVISION_ID)
    for source_id in sqlite_data_revision.get_source_ids():
        with open(get_global_subnational_covid_data_dir() / f'covid_{source_id}.tsv',
                  'w', encoding='utf-8') as f:
            f.write(sqlite_data_revision.get_tsv_data(source_id))

    # Commit to GitHub
    repo = Repo(str(get_global_subnational_covid_data_dir()))
    repo.git.add(update=True)
    repo.index.commit('update data')
    origin = repo.remote(name='origin')
    origin.push()
