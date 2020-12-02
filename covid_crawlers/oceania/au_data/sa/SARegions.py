
# Steps to install (tested only on Ubuntu 18.04 LTS):
# 1. Extract browsermob-proxy-2.1.4-bin.zip from
#    https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4
#    to your home directory
# 2. run "sudo pip3 install browsermob-proxy selenium editdistance psutil"
# 3. Follow the steps at https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
# 4. Run this script with "python3 grab.py"

import os
import time
import json
import base64
import psutil
import brotli
import datetime
from sys import path
from os import makedirs, environ, pathsep, system
from os.path import expanduser
from urllib.request import urlopen
from browsermobproxy import Server
from selenium import webdriver
from covid_19_au_grab._utility.get_package_dir import get_data_dir


BROWSER_MOB_PROXY_LOC = expanduser(
    '~/browsermob-proxy-2.1.4-bin/'
    'browsermob-proxy-2.1.4/bin/'
    'browsermob-proxy'
)
GECKO_BROWSER_DIR = expanduser(
    '~/geckodriver-v0.26.0-linux64/'
)
SA_REGIONS_URL = (
    #'https://dpc.geohub.sa.gov.au/portal/apps/View/index.html?appid=963e7887610146ec813e7889bb658805'
    'https://dpc.geohub.sa.gov.au/portal/apps/View/index.html?appid=1ae1bf4b7b6a46bda4a65b48c2da9406'
)
PATH_PREFIX = get_data_dir() / 'sa' / 'custom_map'


class _SARegions:
    def run_wa_regions(self):
        self.output_dir = self._get_output_json_dir()

        path.append(GECKO_BROWSER_DIR)
        environ["PATH"] += pathsep + GECKO_BROWSER_DIR
        system('killall browsermob-prox')

        for xx, json_data in enumerate(self.__grab()):
            if not isinstance(json_data, bytes):
                with open(
                    f"{self.output_dir}/json_output-{xx}.json",
                    'w', encoding='utf-8'
                ) as f:
                    f.write(json.dumps(json_data, indent=2))
            else:
                with open(
                    f"{self.output_dir}/bin_output-{xx}.pbf", 'wb'
                ) as f:
                    f.write(json_data)

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

        proxy.new_har("file_name", options={'captureHeaders': True,
                                            'captureContent': True,
                                            'captureBinaryContent': True})
        driver.get(SA_REGIONS_URL)
        time.sleep(15)
        for i in range(5):
            # Zoom out a few times
            content = driver.find_element_by_css_selector(
                '.esriSimpleSliderDecrementButton'
            )
            content.click()
            time.sleep(4)

        proxy.wait_for_traffic_to_stop(10, 60)

        r = []
        # print(proxy.har, dir(proxy.har))
        for ent in proxy.har['log']['entries']:
            req = ent['request']
            print(req['url'])

            if req['url'].startswith(
                'https://dpc.geohub.sa.gov.au/server/rest/services/Hosted/'
            ) and 'query?' in req['url']:
                print(ent)
                print(ent.keys())
                if not 'text' in ent['response']['content']:
                    continue

                data = ent['response']['content']['text']
                try:
                    data = base64.b64decode(data)
                except: pass
                try:
                    data = brotli.decompress(data)
                except: pass
                try:
                    data = data.decode('utf-8')
                except: pass

                try:
                    r.append(json.loads(data))
                except UnicodeDecodeError:
                    with urlopen(req['url'].replace('query?f=pbf', 'query?f=json')) as f:
                        r.append(json.loads(f.read().decode('utf-8')))

        server.stop()
        driver.quit()
        return r


def run_sa_regions():
    _SARegions().run_wa_regions()


if __name__ == '__main__':
    run_sa_regions()
