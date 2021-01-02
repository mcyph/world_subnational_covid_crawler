import csv
import json
import requests
from datetime import datetime
from _utility.get_package_dir import get_data_dir


class CacheBase:
    def _get_new_dir(self):
        revision_id = 0
        while True:
            fmt = f'%%y_%%m_%%d-%03d' % revision_id
            child_dir_name = datetime.now().strftime(fmt)
            path = get_data_dir() / self.STATE_NAME / self.SOURCE_ID / child_dir_name

            if path.exists():
                revision_id += 1
                continue
            else:
                path.mkdir()
                return path

    def get_latest_dir(self):
        return sorted((get_data_dir() / self.STATE_NAME / self.SOURCE_ID).iterdir())[-1]

    def get_path_in_latest_dir(self, fnam):
        return self.get_latest_dir() / fnam

    def get_json(self, fnam):
        with open(self.get_path_in_latest_dir(fnam), 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def get_csv(self, fnam, *args, **kw):
        f = open(self.get_path_in_latest_dir(fnam), 'r', encoding='utf-8')
        return csv.DictReader(f, *args, **kw)

    def download_to(self, path, url):
        r = requests.get(
            url,
            headers={
                "USER-AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
                "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "ACCEPT-LANGUAGE": "en-US,en;q=0.5",
                "ACCEPT-ENCODING": "gzip, deflate",  # , br
                "CONNECTION": "keep-alive",
                "REFERER": url,  # FIXME!
                "UPGRADE-INSECURE-REQUESTS": "1",
                "PRAGMA": "no-cache",
                "CACHE-CONTROL": "no-cache",
                "TE": "Trailers",
                "COOKIE": "language=en; _ga=GA1.2.2016181909.1598484966; _gid=GA1.2.1748222623.1599205537; _gat_gtag_UA_125495940_3=1; mzcr-diseases-eu-cookies=1"
                # For Yemen
            },
            verify=False
        )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(r.text)
