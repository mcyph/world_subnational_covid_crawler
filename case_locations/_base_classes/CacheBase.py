from datetime import datetime
from _utility.get_package_dir import get_data_dir


class CacheBase:
    def _get_new_dir(self):
        revision_id = 0
        while True:
            fmt = f'%%y_%%m_%%d-%03d' % revision_id
            child_dir_name = datetime.now().strftime(fmt)
            path = get_data_dir() / self.STATE_NAME / 'case_locs' / child_dir_name

            if path.exists():
                revision_id += 1
                continue
            else:
                path.mkdir()
                return path

