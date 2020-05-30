import csv
from collections import namedtuple
from covid_19_au_grab.get_package_dir import get_package_dir


Coord = namedtuple('Coord', [
    'lat', 'long'
])

ISO3166 = namedtuple('ISO3166', [
    'a2', 'a3', 'n3'
])

COWItem = namedtuple('COWItem', [
    'iso3166',
    'fips104',
    'has_capital',
    'continent',
    'subcontinent',
    'language',
    'population',
    'year',
    'conventional_abbreviation',
    'international_dialing_code',
    'international_vehicle_code',

    'area',
    'coords',
    'max_coords',
    'min_coords',

    'iso',
    'un',
    'ungegn',
    'bgn',
    'pcgn',
    'fao',
    'eki',
    'url',
])


def _get_data_items():
    r = []

    f = open(get_package_dir() / 'other_data' / 'iso_3166_1' / 'cow.csv',
             'r', encoding='utf-8')

    for item in csv.DictReader(
        filter(lambda row: row[0]!='#', f),
        delimiter=';'
    ):  
        for k in item:
            item[k] = item[k].strip()
        
        r.append(COWItem(**dict(
            iso3166=ISO3166(
                a2=item['ISO3166A2'],
                a3=item['ISO3166A3'],
                n3=item['ISO3166N3']
            ),
            fips104=item['FIPS104'],

            has_capital=item['HasCapital'],
            continent=item['continent'],
            subcontinent=item['subcontinent'],
            language=item['language'],
            population=int(item['population']),
            year=item['year'],
            conventional_abbreviation=item['conabbr'],

            international_dialing_code=item['ITU'],
            international_vehicle_code=item['IVC'],

            area=dict(
                land=item['land'],
                water=item['water'],
                lang_total=item['land_total']
            ),
            coords=Coord(
                float(item['latitude']),
                float(item['longitude'])
            ),
            max_coords=Coord(
                float(item['maxlatitude']),
                float(item['maxlongitude'])
            ),
            min_coords=Coord(
                float(item['minlatitude']),
                float(item['minlongitude'])
            ),

            iso=dict(
                name=dict(
                    en=item['ISOen_name'],
                    en_romanized=item['ISOen_ro_name'],
                    fr=item['ISOfr_name'],
                    es=item['ISOes_name']
                ),
                proper=dict(
                    en=item['ISOen_proper'],
                    en_romanized=item['ISOen_ro_proper'],
                    fr=item['ISOfr_proper']
                ),
                region=dict(
                    region=item['ISOregion'],
                    subregion=item['ISOsubregion']
                )
            ),
            un=dict(
                en=item['UNen_capital'],
                fr=item['UNfr_capital'],
                es=item['UNes_capital'],
                ru=item['UNru_capital'],
                capital_coords=Coord(
                    float(item['UNc_latitude']),
                    float(item['UNc_longitude'])
                ) if item['UNc_latitude'].strip() else None
            ),
            ungegn=dict(
                name=dict(
                    en=item['UNGEGNen_name'],
                    fr=item['UNGEGNfr_name'],
                    es=item['UNGEGNes_name'],
                    ru=item['UNGEGNru_name'],
                    native_romanized=item['UNGEGNlc_ro_name']
                ),
                longname=dict(
                    en=item['UNGEGNen_longname'],
                    fr=item['UNGEGNfr_longname'],
                    es=item['UNGEGNes_longname'],
                    ru=item['UNGEGNru_longname'],
                    native_romanized=item['UNGEGNlc_ro_longname']
                ),
                capital_romanized=item['UNGEGNlc_capital'],
            ),
            bgn=dict(
                name=dict(
                    en=item['BGN_name'],
                    native_romanized=item['BGNlc_name']
                ),
                proper=dict(
                    en=item['BGN_proper']
                ),
                longname=dict(
                    en=item['BGN_longname'],
                    en_romanized=item['BGNlc_longname']
                ),
                capital=item['BGN_capital'],
                capital_coords=Coord(
                    float(item['BGNc_latitude']),
                    float(item['BGNc_longitude'])
                ),
                demonym=item['BGN_demonym'],
                demonym_adjective=item['BGN_demomyn_adj']
            ),
            pcgn=dict(
                name=item['PCGN_name'],
                proper=item['PCGN_proper'],
                longname=item['PCGN_longname']
            ),
            fao=dict(
                name=item['FAOit_name'],
                proper=item['FAOit_proper'],
                longname=item['FAOit_longname']
            ),
            eki=dict(
                name=item['EKI_name'],
                longname=item['EKI_longname'],
                capital=item['EKI_capital']
            ),
            url=dict(
                url_gov=item['url_gov'],
                url_stats=item['url_stats'],
                url_gis=item['url_gis'],
                url_post=item['url_post']
            )
        )))

    return r


def _get_data_items_by_name():
    r = {}
    for i in _get_data_items():
        for en_name in (
            i.iso['name']['en'],
            i.iso['proper']['en'],
            i.un['en'],
            i.ungegn['name']['en'],
            i.ungegn['longname']['en'],
            i.bgn['name']['en'],
            i.bgn['proper']['en'],
            i.bgn['longname']['en']
        ):
            en_name = en_name.lower()
            if not en_name:
                continue

            assert r.get(en_name, i) == i, (en_name, i)
            r[en_name] = i
    return r


def _get_data_items_by_code():
    r = {}
    for i in _get_data_items():
        for code in (
            i.iso3166.a2,
            i.iso3166.a3,
            i.iso3166.n3
        ):
            code = code.lower()
            if not code:
                continue

            assert r.get(code, i) == i, (code, i)
            r[code] = i
    return r


_data_items_by_name = _get_data_items_by_name()
_data_items_by_code = _get_data_items_by_code()


def get_data_item_by_code(code):
    return _data_items_by_code[code.lower()]


def get_data_item_by_name(name):
    return _data_items_by_name[name.lower()]


if __name__ == '__main__':
    from pprint import pprint
    pprint(_get_data_items_by_name())
    print(get_data_item_by_code('au'))
    print(get_data_item_by_code('usa'))
    print(get_data_item_by_name('australia'))
