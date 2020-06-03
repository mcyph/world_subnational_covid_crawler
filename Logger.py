import datetime

from covid_19_au_grab.db.RevisionIDs import RevisionIDs


TIME_FORMAT = datetime.datetime \
                      .now() \
                      .strftime('%Y_%m_%d')


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
