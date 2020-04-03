from os import listdir
from os.path import expanduser

from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_BY_REGION, DT_AGE, DT_AGE_MALE, DT_AGE_FEMALE, DT_SOURCE_OF_INFECTION


BASE_PATH = expanduser('~/dev/covid_19_data/vic/powerbi')
SOURCE_URL = 'https://app.powerbi.com/view?r=' \
             'eyJrIjoiODBmMmE3NWQtZWNlNC00OWRkLTk1NjYtM' \
             'jM2YTY1MjI2NzdjIiwidCI6ImMwZTA2MDFmLTBmYW' \
             'MtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9'


def get_powerbi_data():
    output = []

    for dir_ in listdir(BASE_PATH):
        subdir = f'{BASE_PATH}/{dir_}'

        for fnam in listdir(subdir):
            path = f'{subdir}/{fnam}'
            #print(path)
            with open(path, 'r', encoding='utf-8') as f:
                from json import loads
                data = loads(f.read())

            if fnam == 'regions.json':
                #print(data['results'][0]['result']['data'])
                for region in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
                    print(region)
                    output.append(DataPoint(
                        name=region['C'][0].split('(')[0].strip(),
                        datatype=DT_CASES_BY_REGION,
                        value=region['C'][1]
                              if len(region['C']) >= 2
                              else 0,
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))

            elif fnam == 'age_data.json':
                for age in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
                    print(age)
                    if not age['X'] or not 'M0' in age['X'][0]:
                        print("WARNING:", age)
                        continue

                    X = [i for i in age['X'] if not 'S' in i][:2]    # WARNING!!!!

                    if len(X) == 2:
                        output.append(DataPoint(
                            name=age['G0'].replace('–', '-'),
                            datatype=DT_AGE_MALE,
                            value=X[0].get('M0', 0),
                            date_updated=dir_.split('-')[0],
                            source_url=SOURCE_URL,
                            text_match=None
                        ))
                        output.append(DataPoint(
                            name=age['G0'].replace('–', '-'),
                            datatype=DT_AGE_FEMALE,
                            value=X[1].get('M0', 0),
                            date_updated=dir_.split('-')[0],
                            source_url=SOURCE_URL,
                            text_match=None
                        ))
                        general_age = (
                            X[0].get('M0', 0) +
                            X[1].get('M0', 0)
                        )
                    elif len(age['X']) == 1:
                        pass
                    else:
                        raise Exception(age)

                    output.append(DataPoint(
                        name=age['G0'].replace('–', '-'),
                        datatype=DT_AGE,
                        value=general_age,
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))

            elif fnam == 'source_of_infection.json':
                for source in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
                    output.append(DataPoint(
                        name=source['C'][0],
                        datatype=DT_SOURCE_OF_INFECTION,
                        value=source['C'][1],
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))

    return output