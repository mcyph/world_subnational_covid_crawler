import sys
import json
import datetime
from os import system

from _utility.Logger import Logger
from _utility.get_package_dir import get_output_dir
from covid_crawlers._base_classes.OverseasDataSources import OverseasDataSources
from covid_crawlers.oceania.au_data.StateDataSources import StateDataSources
from covid_crawlers.oceania.au_data.InfrequentStateDataJobs import InfrequentStateDataJobs

from covid_db.RevisionIDs import RevisionIDs
from covid_db.DerivedData import DerivedData
from covid_db.DataPointsDB import DataPointsDB
from covid_db.delete_old_dbs import delete_old_dbs
from covid_db.SQLiteDataRevisions import SQLiteDataRevisions
from covid_db.output_compressor.output_revision_datapoints_to_zip import output_revision_datapoints_to_zip
from _utility.output_tsv_data import output_tsv_data, output_source_info, output_geojson, push_to_github


OUTPUT_DIR = get_output_dir() / 'output'
TIME_FORMAT = datetime.datetime.now().strftime('%Y_%m_%d')
LATEST_REVISION_ID = RevisionIDs.get_latest_revision_id(TIME_FORMAT)
RUN_INFREQUENT_JOBS = '--run-infrequent-jobs' in [i.strip() for i in sys.argv]
SOURCE_INFO = []


def run_infrequent_jobs():
    """
    Run infrequent tasks which require more resources
    Comment out any of these if they break!
    """
    isdj = InfrequentStateDataJobs()
    isdj.update_wa_regions()
    isdj.update_vic_tableau()
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
        SOURCE_INFO.append([source_id, source_url, source_desc])
        dpdb.extend(source_id, _rem_dupes(datapoints), is_derived=False)

    return ods.get_status_dict()


def output_state_data(dpdb):
    """
    Output from state data
    """
    sds = StateDataSources()

    for source_id, source_url, source_desc, datapoints in sds.iter_data_sources():
        SOURCE_INFO.append([source_id, source_url, source_desc])
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
    if True:
        print("Outputting state data...")
        status.update(output_state_data(dpdb))
        print("State data done. Outputting overseas data...")
        status.update(output_overseas_data(dpdb))
        print("Overseas data done. Migrating sources with errors...")
    else:
        # WARNING!!!! THIS CODE HAS BUGS+DOESN'T OUTPUT THE CASES!!!! ===============================================
        print("Outputting state and overseas data...")
        _output_state_data = lambda: status.update(output_state_data(dpdb))
        _output_overseas_data = lambda: status.update(output_overseas_data(dpdb))
        t1 = threading.Thread(target=_output_state_data, args=())
        t2 = threading.Thread(target=_output_overseas_data, args=())
        t1.start(); t2.start()
        t1.join(); t2.join()
        print("State and overseas data done. Migrating sources with errors...")

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
    print("Derived data outputted OK: committing and closing")
    dpdb.commit()
    dpdb.close()

    # Output basic status info to a .json info
    # This also signifies to the web
    # interface that the import went OK
    print("Writing status JSON file")
    status_json_path = RevisionIDs.get_path_from_id(
        TIME_FORMAT, LATEST_REVISION_ID, 'json'
    )
    with open(status_json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'status': status}, indent=4))

    # Output datapoints to zip
    print("Outputting datapoints to zip...")
    with open(get_output_dir() / 'output' / f'{TIME_FORMAT}-{LATEST_REVISION_ID}.zip', 'wb') as f:
        output_revision_datapoints_to_zip(f, TIME_FORMAT, LATEST_REVISION_ID)

    # Upload them to remote AWS instance
    print("Uploading zip file to remote server...")
    system('/usr/bin/env bash /home/david/upload_to_remote.sh %s' % f'{TIME_FORMAT}-{LATEST_REVISION_ID}')

    # Clean up old DBs to save on space
    print("Deleting older DBs to save space..")
    delete_old_dbs()

    # Update the csv output
    print("Outputting TSV files:")
    output_tsv_data(TIME_FORMAT, LATEST_REVISION_ID)
    print('TSV write done')

    # Output information about the sources to a markdown table/csv file
    print("Outputting source info...")
    output_source_info(SOURCE_INFO)

    # Output GeoJSON
    print("Outputting geojson...")
    output_geojson()

    # Commit to GitHub
    print("Pushing to GitHub...")
    push_to_github()
    print("Push to GitHub done!")

    print("[end of script]")
