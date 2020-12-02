
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
WA_REGIONS_URL = (
    #'https://ww2.health.wa.gov.au/Articles/'
    #'A_E/Coronavirus/COVID19-statistics'
    'https://experience.arcgis.com/experience/359bca83a1264e3fb8d3b6f0a028d768'
)


URL_REGIONS = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/confirmed_cases_by_LGA_view_layer/FeatureServer/0/query'
URL_SOURCE_OF_INFECTION = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/Epidemic_curve_date_new_view_layer/FeatureServer/0/query?f=json&where=Total_Confirmed%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&outSR=102100&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'
URL_OTHER_STATS = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/COVID19_Dashboard_Chart_ViewLayer/FeatureServer/0/query?f=json&where=new_cases%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=date%20asc&outSR=102100&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'
URL_MF_BALANCE = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/Age_sex_total_COVID19_Chart_view_layer/FeatureServer/0/query?f=json&where=Age_Group%3D%27Total%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true'
URL_AGE_BALANCE = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/Age_sex_total_COVID19_Chart_view_layer/FeatureServer/0/query?f=json&where=Age_Group%3C%3E%27Total%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'


PATH_PREFIX = get_data_dir() / 'wa' / 'custom_dash'


class _WADash:
    def run_wa_dash(self):
        self.output_dir = self._get_output_json_dir()

        path.append(GECKO_BROWSER_DIR)
        environ["PATH"] += pathsep + GECKO_BROWSER_DIR
        system('killall browsermob-prox')

        self.__grab()

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
        driver.get(WA_REGIONS_URL)
        time.sleep(50)
        proxy.wait_for_traffic_to_stop(10, 60)

        r = []
        # print(proxy.har, dir(proxy.har))
        for ent in proxy.har['log']['entries']:
            req = ent['request']
            #print(req['url'])

            for fnam_prefix, url in (
                ('regions', URL_REGIONS),
                ('infection_source', URL_SOURCE_OF_INFECTION),
                ('other_stats', URL_OTHER_STATS),
                ('mf_balance', URL_MF_BALANCE),
                ('age_balance', URL_AGE_BALANCE)
            ):
                if url == URL_REGIONS and req['url'].startswith(URL_REGIONS):
                    pass
                elif url == req['url']:
                    pass
                else:
                    continue

                #print(ent)
                #print(ent.keys())
                if not 'text' in ent['response']['content']:
                    continue

                data = brotli.decompress(
                    base64.b64decode(ent['response']['content']['text'])
                )
                try:
                    data = (
                        json.loads(data.decode('utf-8'))
                    )
                except UnicodeDecodeError:
                    with urlopen(req['url'].replace('query?f=pbf', 'query?f=json')) as f:
                        data = json.loads(f.read().decode('utf-8'))

                with open(
                    f"{self.output_dir}/{fnam_prefix}.json",
                    'w', encoding='utf-8'
                ) as f:
                    f.write(json.dumps(data, indent=2))


        server.stop()
        driver.quit()
        return r


def run_wa_dash():
    _WADash().run_wa_dash()


if __name__ == '__main__':
    run_wa_dash()
