import json
from collections import Counter
from datetime import datetime, timedelta
from urllib.request import urlretrieve
from os import makedirs, listdir
from os.path import exists

from _utility.get_package_dir import get_data_dir
from _utility.cache_by_date import cache_by_date
from covid_db.datatypes.DataPoint import DataPoint
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DatapointMerger import DataPointMerger
from covid_crawlers.oceania.au_data.nsw.NSWJSONOpenData import POSTCODE_TO_LGA, NSWJSONOpenData


class NSWJSONWebsiteData:
    SOURCE_ID = 'au_nsw_website_data'
    SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data'
    SOURCE_DESCRIPTION = ''

    def get_datapoints(self):
        if not POSTCODE_TO_LGA:
            # HACK: Make sure postcode -> lga map is available!
            NSWJSONOpenData().get_datapoints()

        date = (
            datetime.now() - timedelta(hours=20, minutes=30)
        ).strftime('%Y_%m_%d')

        dates = sorted(listdir(get_data_dir() / 'nsw' / 'open_data'))
        if not date in dates:
            dates.append(date)

        website_data = DataPointMerger()
        for i_date in dates:
            download = i_date == date
            for datapoint in self.__get_website_datapoints(i_date, download=download):
                website_data.append(datapoint)

        r = []
        r.extend(website_data)
        return r

    @cache_by_date(SOURCE_ID)
    def __get_website_datapoints(self, date, download=True):
        dir_ = get_data_dir() / 'nsw' / 'open_data' / date
        if not exists(dir_):
            makedirs(dir_)

        # Add website data
        website_data = []
        website_data.extend(self.get_nsw_postcode_data(dir_, download=download))
        website_data.extend(self.__postcode_datapoints_to_lga('https://data.nsw.gov.au/nsw-covid-19-data', website_data,
                                                              source_id=self.SOURCE_ID))
        # Age distributions
        website_data.extend(self.get_nsw_age_data(dir_, date, download=download))
        return website_data

    def __postcode_datapoints_to_lga(self, SOURCE_URL, r, source_id):
        # Convert postcode to LGA where possible
        new_r = DataPointMerger()
        added_to_lga = set()
        processed_postcode = set()
        mapping = Counter()

        for datapoint in sorted(r, key=lambda i: i.date_updated):
            if datapoint.region_schema == Schemas.LGA:
                added_to_lga.add((
                    datapoint.region_child,
                    datapoint.datatype
                ))
                continue
            elif datapoint.region_schema != Schemas.POSTCODE:
                continue
            elif datapoint.region_child in POSTCODE_TO_LGA:
                lga = POSTCODE_TO_LGA[datapoint.region_child]
            else:
                lga = 'unknown'
                if datapoint.region_child != 'unknown':
                    print("NOT FOUND:", datapoint.region_child)
                # continue  # WARNINIG!!! ================================================================================

            if (datapoint.region_child, datapoint.datatype, datapoint.date_updated) in processed_postcode:
                #print("IGNORING DOUBLE-UP:", datapoint)
                continue
            processed_postcode.add((datapoint.region_child, datapoint.datatype, datapoint.date_updated))

            #if lga == 'cumberland':
            #    print('USING:', datapoint)

            mapping[
                lga,
                datapoint.datatype,
                datapoint.date_updated
            ] += datapoint.value

        new_r.extend(r)

        for (lga, datatype, date_updated), value in mapping.items():
            if (lga, datatype) in added_to_lga:
                # Don't add to LGA if available using direct data!
                continue

            new_r.append(DataPoint(
                region_schema=Schemas.LGA,
                region_parent='AU-NSW',
                region_child=lga,
                datatype=datatype,
                value=value,
                date_updated=date_updated,
                source_url=SOURCE_URL,
                source_id=source_id
            ))

        return new_r

    #=============================================================================#
    # Postcode-level website json data
    #=============================================================================#

    def get_nsw_age_data(self, dir_, date, download=True):
        r = DataPointMerger()

        path_fatalitiesdata = dir_ / 'fatalitiesdata.json'
        path_agedata = dir_ / 'agedata.json'
        path_listing = dir_ / 'find-facts-about-covid-19.html'

        if not exists(path_fatalitiesdata) or not exists(path_agedata) or not exists(path_listing):
            if not download:
                return []

            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/fatalitiesdata.json',
                path_fatalitiesdata
            )
            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/agedata.json',
                path_agedata
            )
            urlretrieve(
                'https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                path_listing
            )

        if False:
            # This actually could be unreliable - it's on an external web service even though on the
            # same page and suspect doesn't necessarily get updated at the same as other elements on the page

            with open(path_listing, 'r', encoding='utf-8') as f:
                html = f.read()
                try:
                    _date = html.split('Last updated')[1].strip().partition(' ')[-1].split('.')[0].strip()
                    date = datetime.strptime(_date, '%d %B %Y').strftime('%Y_%m_%d')
                except IndexError:
                    # It seems this info isn't always supplied(?) =============================================================
                    import traceback
                    traceback.print_exc()

        with open(path_agedata, 'r', encoding='utf-8') as f:
            # {"data":[{"ageGroup":"0-9","Males":null,"Females":null},
            agedata = json.loads(f.read())

            for age_dict in agedata['data']:
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AU',
                    region_child='AU-NSW',
                    datatype=DataTypes.TOTAL_MALE,
                    value=age_dict['Males'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None,
                    source_id=self.SOURCE_ID
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AU',
                    region_child='AU-NSW',
                    datatype=DataTypes.TOTAL_FEMALE,
                    value=age_dict['Females'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None,
                    source_id=self.SOURCE_ID
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AU',
                    region_child='AU-NSW',
                    datatype=DataTypes.TOTAL,
                    value=(age_dict['Females'] or 0) + (age_dict['Males'] or 0),
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None,
                    source_id=self.SOURCE_ID
                ))

        """
        with open(path_fatalitiesdata, 'r', encoding='utf-8') as f:
            agedata = json.loads(f.read())

            for age_dict in agedata['data']:
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AU',
                    region_child='AU-NSW',
                    datatype=DataTypes.STATUS_DEATHS_MALE,
                    value=age_dict['Males'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None,
                    source_id=self.SOURCE_ID_WEBSITE_DATA
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AU',
                    region_child='AU-NSW',
                    datatype=DataTypes.STATUS_DEATHS_FEMALE,
                    value=age_dict['Females'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None,
                    source_id=self.SOURCE_ID_WEBSITE_DATA
                ))
        """

        return r

    #=============================================================================#
    # Postcode-level website tests json data
    #=============================================================================#

    def get_nsw_postcode_data(self, dir_, download=True):
        # {"data":[{"Recovered":5,"POA_NAME16":"2106","Deaths":0,"Cases":5,"Date":"14-May"},

        path_totals = dir_ / 'covid_19_cases_by_postcode_totals.json'
        path_active_deaths = dir_ / 'covid_19_cases_by_postcode_active_deaths.json'
        path_tests = dir_ / 'covid_19_tests_by_postcode.json'
        path_active = dir_ / 'covid_19_cases_by_postcode_active.json'

        if not exists(path_totals) or not exists(path_active_deaths) or not exists(path_active) or not exists(path_tests):
            if download:
                # Retrieve these, just in cases...
                urlretrieve(
                    'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/data_Cases2.json',
                    path_active_deaths
                )
                urlretrieve(
                    'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/data_Cases.json',
                    path_totals
                )
                urlretrieve(
                    'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/data_tests.json',
                    path_tests
                )
                urlretrieve(
                    'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/active_cases.json',
                    path_active
                )

        r = []
        SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data/tests'

        if exists(path_active):
            active_data = self.__get_active_data(path_active)
        else:
            active_data = {}

        if exists(path_active_deaths):
            r.extend(self.__get_active_deaths_datapoints(SOURCE_URL, path_active_deaths, active_data))

        #r.extend(self.__get_tests_datapoints(SOURCE_URL, path_tests))  # NOTE ME: Will use open data for tests!! ===============

        if exists(path_totals):
            r.extend(self.__get_totals_datapoints(SOURCE_URL, path_totals))

        return r

    def __get_active_data(self, path_active):
        r = {}
        with open(path_active, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                # {"data":[{
                #   "Day11":0,"Day12":0,"Day13":0,"POA_NAME16":"2541",
                #   "Day0":0,"Day1":0,"Day2":0,"Day3":0,"Day10":0,"Day4":0,
                #   "Day5":0,"Day6":0,"Day7":0,"Day8":0,"Day9":0},
                for x in range(14):
                    r.setdefault(item['POA_NAME16'], []).append(item[f'Day{x}'])
        return r

    def __get_active_deaths_datapoints(self, SOURCE_URL, path_active_deaths, active_data):
        r = DataPointMerger()

        with open(path_active_deaths, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                date = datetime.strptime(item['Date'] + '-20', '%d-%b-%y').strftime('%Y_%m_%d')
                recovered = int(item['Recovered'])
                deaths = int(item['Deaths'])
                cases = int(item['Cases'])
                censored = int(item.get('censored',
                                        0))  # NOTE ME:  From 12 June, this heatmap reporting of active cases has changed. Cases that are not recorded as recovered or deceased after six weeks are not included.
                active = cases - recovered - deaths - censored
                postcode = item['POA_NAME16'] if item['POA_NAME16'] else 'Unknown'

                r.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DataTypes.TOTAL,
                    value=cases,
                    date_updated=date,
                    source_url=SOURCE_URL,
                    source_id=self.SOURCE_ID
                ))

                if postcode in active_data:
                    num_active = active_data[postcode].pop()

                    r.append(DataPoint(
                        region_schema=Schemas.POSTCODE,
                        region_parent='AU-NSW',
                        region_child=postcode,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=num_active, # CHECK ME!!!!! =====================================
                        date_updated=date,
                        source_url=SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))

                    r.append(DataPoint(
                        region_schema=Schemas.POSTCODE,
                        region_parent='AU-NSW',
                        region_child=postcode,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=cases-num_active-deaths,  # CHECK ME!!!!! =====================================
                        date_updated=date,
                        source_url=SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))
                elif date <= '2020_06_12':
                    r.append(DataPoint(
                        region_schema=Schemas.POSTCODE,
                        region_parent='AU-NSW',
                        region_child=postcode,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=active,
                        date_updated=date,
                        source_url=SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))

                #r.append(DataPoint(
                #    region_schema=Schemas.POSTCODE,
                #    region_parent='AU-NSW',
                #    region_child=postcode,
                #    datatype=DataTypes.STATUS_RECOVERED,
                #    value=recovered,
                #    date_updated=date,
                #    source_url=SOURCE_URL
                #))
                r.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=deaths,
                    date_updated=date,
                    source_url=SOURCE_URL,
                    source_id=self.SOURCE_ID
                ))

        return r

    def __get_tests_datapoints(self, SOURCE_URL, path_tests):
        r = DataPointMerger()

        with open(path_tests, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                date = datetime.strptime(item['Date'] + '-20', '%d-%b-%y').strftime('%Y_%m_%d')
                number = int(item['Number'])
                # recent = item['Recent'] # TODO: ADD ME!!! ========================================================
                postcode = item['POA_NAME16'] if item['POA_NAME16'] else 'Unknown'

                r.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DataTypes.TESTS_TOTAL,
                    value=number,
                    date_updated=date,
                    source_url=SOURCE_URL,
                    source_id=self.SOURCE_ID
                ))

        return r

    def __get_totals_datapoints(self, SOURCE_URL, path_totals):
        # Pretty sure this is dupe data (for now)
        # Don't uncomment this without making sure this won't double the result(!)
        r = DataPointMerger()

        with open(path_totals, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                date = datetime.strptime(item['Date'] + '-20', '%d-%b-%y').strftime('%Y_%m_%d')
                number = int(item['Number'])
                postcode = item['POA_NAME16'] if item['POA_NAME16'] else 'Unknown'

                r.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DataTypes.TOTAL,
                    value=number,
                    date_updated=date,
                    source_url=SOURCE_URL,
                    source_id=self.SOURCE_ID
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = NSWJSONWebsiteData()
    pprint(inst.get_datapoints())
