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
import psutil
import datetime
import editdistance
from sys import path
from os import makedirs, environ, pathsep, system
from os.path import dirname, expanduser
from browsermobproxy import Server
from selenium import webdriver


BROWSER_MOB_PROXY_LOC = expanduser(
    '~/browsermob-proxy-2.1.4-bin/'
    'browsermob-proxy-2.1.4/bin/'
    'browsermob-proxy'
)
GECKO_BROWSER_DIR = expanduser(
    '~/geckodriver-v0.26.0-linux64/'
)


class PowerBIBase:
    def __init__(self, path_prefix, globals_dict, powerbi_url, num_pages=4):
        self.path_prefix = path_prefix
        self.globals_dict = globals_dict
        self.powerbi_url = powerbi_url
        self.num_pages = num_pages

    def run_powerbi_grabber(self):
        self.output_dir = self._get_output_json_dir()

        path.append(GECKO_BROWSER_DIR)
        environ["PATH"] += pathsep + GECKO_BROWSER_DIR
        system('killall browsermob-prox')

        # grab()
        self.match_grabbed_with_types()

    def match_grabbed_with_types(self):
        r = []

        for post_data, content in self.__grab():
            prefix_suffix = 1
            while True:
                path = f'{self.output_dir}/json_data-{prefix_suffix}.json'
                if not os.path.exists(path):
                    break
                prefix_suffix += 1

            with open(path, 'w',
                      encoding='utf-8',
                      errors='replace') as f:
                f.write(json.dumps(
                    [post_data, content],
                    indent=2,
                    sort_keys=True
                ))
        return r

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

            dir_ = f'{self.path_prefix}/{time_format}-{revision_id}'
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
                                            'captureContent': True})
        driver.get(self.powerbi_url)

        for x in range(self.num_pages):
            time.sleep(25)

            proxy.wait_for_traffic_to_stop(10, 60)

            # Go to the next page
            content = driver.find_element_by_css_selector(
                '.glyphicon.glyph-small.pbi-glyph-chevronrightmedium.middleIcon'
            )
            content.click()

        proxy.wait_for_traffic_to_stop(10, 60)

        r = []
        # print(proxy.har, dir(proxy.har))
        for ent in proxy.har['log']['entries']:
            req = ent['request']
            # print(req['url'])
            if req['url'] == 'https://wabi-australia-southeast-api.analysis.windows.net/' \
                             'public/reports/querydata' or \
               req['url'].split('?')[0] == 'https://wabi-north-europe-api.analysis.windows.net/' \
                                           'public/reports/querydata':

                if not 'postData' in req:
                    #print("ignoring:", req)
                    continue

                # print(req.keys())
                # print(ent.keys())
                # print(ent)
                # print(req['postData'])
                # print(ent['response'])
                # print()

                r.append((
                    json.loads(req['postData']['text']),
                    json.loads(ent['response']['content']['text'])
                ))

        server.stop()
        driver.quit()
        return r
