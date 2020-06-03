import os
from os import makedirs
from os.path import dirname

from covid_19_au_grab.get_package_dir import get_package_dir


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
            get_package_dir() / 'output' /
                f'{time_format}-{revision_id}.{ext}'
        )
