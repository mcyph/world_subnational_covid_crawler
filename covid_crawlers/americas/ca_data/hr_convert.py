import csv
from covid_19_au_grab._utility.get_package_dir import get_package_dir

HR_MAP_PATH = get_package_dir() / 'covid_crawlers' / 'americas' / 'ca_data' / 'hr_map.csv'


_province_map = {
    'Alberta': 'CA-AB',
    'BC': 'CA-BC',
    'Manitoba': 'CA-MB',
    'New Brunswick': 'CA-NB',
    'NL': 'CA-NL',
    'Nova Scotia': 'CA-NS',
    'Nunavut': 'CA-NU',
    'NWT': 'CA-NT',
    'Ontario': 'CA-ON',
    'PEI': 'CA-PE',
    'Quebec': 'CA-QC',
    'Saskatchewan': 'CA-SK',
    'Yukon': 'CA-YT',
    'Repatriated': 'other',
}


def _get_hr_map():
    uid_to_hr = {}
    hr_to_uid = {}

    with open(HR_MAP_PATH, 'r', encoding='utf-8') as f:
        for item in csv.DictReader(f):
            province = _province_map[item['Province']]
            uid_to_hr[item['HR_UID']] = (province, item['health_region'])
            hr_to_uid[province.lower(), item['health_region'].lower()] = item['HR_UID']

    return uid_to_hr, hr_to_uid


_uid_to_hr, _hr_to_uid = _get_hr_map()


def province_to_iso_3166_2(province):
    return _province_map[province]


def health_region_to_uid(iso_3166_2_province, hr):
    iso_3166_2_province = _province_map.get(
        iso_3166_2_province, iso_3166_2_province
    )
    if hr.lower() == 'not reported':
        return 'Unknown'
    return _hr_to_uid[iso_3166_2_province.lower(), hr.lower()]


def uid_to_health_region(uid):
    # Convert to Canada Health Region from the health region unique ID
    return _uid_to_hr[str(uid)]

