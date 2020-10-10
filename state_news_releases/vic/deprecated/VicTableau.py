import os
import time
import json
import base64
import psutil
import brotli
import datetime
from sys import path
from os import makedirs, environ, pathsep, system
from os.path import dirname, expanduser
from urllib.request import urlopen
from browsermobproxy import Server
from selenium import webdriver
from covid_19_au_grab.get_package_dir import get_data_dir


BROWSER_MOB_PROXY_LOC = expanduser(
    '~/browsermob-proxy-2.1.4-bin/'
    'browsermob-proxy-2.1.4/bin/'
    'browsermob-proxy'
)
GECKO_BROWSER_DIR = expanduser(
    '~/geckodriver-v0.26.0-linux64/'
)
PATH_PREFIX = get_data_dir() / 'vic' / 'tableau'


JSON_URL_INCLUDES = '/sessions/'

TRANSMISSIONS_OVER_TIME_URL = 'https://public.tableau.com/profile/vicdhhs#!/vizhome/Transmissionsovertime/DashboardPage'
TRANSMISSIONS_URL = 'https://public.tableau.com/profile/vicdhhs#!/vizhome/Transmissions/dashpage'
AGEGROUP_URL = 'https://public.tableau.com/profile/vicdhhs#!/vizhome/Agegroup_15982346382420/DashboardPage'


class _VicTableau:
    def run_vic_tableau(self):
        self.output_dir = self._get_output_json_dir()

        path.append(GECKO_BROWSER_DIR)
        environ["PATH"] += pathsep + GECKO_BROWSER_DIR
        system('killall browsermob-prox')

        json_data = self.__grab()
        with open(f"{self.output_dir}/output.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data, indent=4))

    def _get_output_json_dir(self):
        time_format = datetime.datetime \
            .now() \
            .strftime('%Y_%m_%d')

        # Get a revision id
        x = 0
        revision_id = 1

        while True:
            if x > 1000:
                # This should never happen, but still..
                raise Exception()

            dir_ = f'{PATH_PREFIX}/{time_format}-{revision_id}'
            if not os.path.exists(dir_):
                break

            revision_id += 1
            x += 1

        try:
            makedirs(dir_)
        except OSError:
            pass
        return dir_

    def __grab(self):
        # Destroy any previous instances of browsermob-proxy
        for proc in psutil.process_iter():
            # print(proc.name())
            if proc.name() in ("browsermob-proxy",
                               "browsermob-prox"):
                print("Killing proc:", proc.name())
                proc.kill()

        print("Creating Server...")
        server = Server(BROWSER_MOB_PROXY_LOC)
        server.start()
        time.sleep(1)

        print("Creating Proxy...")
        proxy = server.create_proxy(params={'port': 9770})
        time.sleep(1)

        print("Creating Selenium/Chrome...")
        args = [
            "--proxy-server=localhost:%s" % proxy.port,
            '--ignore-certificate-errors',
            '--disable-dev-shm-usage',

            '--disable-extensions',
            '--disable-gpu',
            '--no-sandbox',
            #'--headless',
        ]
        chrome_options = webdriver.ChromeOptions()
        for arg in args:
            chrome_options.add_argument(arg)
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1400, 1050)

        proxy.new_har("file_name", options={
            'captureHeaders': True,
            'captureContent': True,
            'captureBinaryContent': True
        })

        r = {}
        for key, url in (
            ('transmissions_over_time', TRANSMISSIONS_OVER_TIME_URL),
            ('transmissions', TRANSMISSIONS_URL),
            ('agegroup', AGEGROUP_URL)
        ):
            driver.get(url)
            time.sleep(20)
            proxy.wait_for_traffic_to_stop(10, 60)

            item = []
            # print(proxy.har, dir(proxy.har))
            for ent in proxy.har['log']['entries']:
                req = ent['request']

                if JSON_URL_INCLUDES in req['url']:
                    #print("USING:", req['url'])
                    # print(ent)
                    # print(ent.keys())
                    #print(ent['response']['content'])

                    data = ent['response']['content']['text']
                    try:
                        data = base64.b64decode(data)
                    except: pass
                    try:
                        data = data.decode('utf-8')
                    except: pass

                    item.append([req['url'], data])
                else:
                    print("IGNORING:", req['url'])

            r[key] = item

        server.stop()
        driver.quit()
        return r


def run_vic_tableau():
    _VicTableau().run_vic_tableau()


if __name__ == '__main__':
    run_vic_tableau()
