# https://data.humdata.org/dataset/europe-covid-19-subnational-cases

import csv

from covid_crawlers._base_classes.URLBase import URL, URLBase
from _utility.get_package_dir import get_overseas_dir

from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import (
    StrictDataPointsFactory, MODE_STRICT
)
from covid_crawlers.world.eu_subnational_data.world_eu_mappings import (
    world_eu_mappings
)

# https://proxy.hxlstandard.org/data/e2bb4b/download/jrc-covid-19-regions-hxl.csv
#
# Date,iso3,CountryName,Region,lat,lon,CumulativePositive,
# CumulativeDeceased,CumulativeRecovered,CurrentlyPositive,
# Hospitalized,IntensiveCare,EUcountry,EUCPMcountry
#
# #date,#country+code+iso3,#country+name,#adm1+name,#geo+lat,#geo+lon,
# #affected+positive+total,#affected+dead+total,#affected+recovered+total,
# #affected+positive,#affected+hospitalized,#affected+intensive_care,
# #indicator+eu,#indicator+eucpm
#
# 2020-01-24,FRA,France,Île-de-France,48.709229,2.503473,2,0,0,2,2,0,TRUE,TRUE
# 2020-01-24,FRA,France,Nouvelle-Aquitaine,45.479897,0.410462,1,0,0,1,1,0,TRUE,TRUE
# 2020-01-25,FRA,France,Île-de-France,48.709229,2.503473,2,0,0,2,2,0,TRUE,TRUE
# 2020-01-25,FRA,France,Nouvelle-Aquitaine,45.479897,0.410462,1,0,0,1,1,0,TRUE,TRUE

OVERRIDES = {
    'Poland': [
        ['PL-DS', 'Dolnośląskie'],
        ['PL-KP', 'Kujawsko-pomorskie'],
        ['PL-LU', 'Lubelskie'],
        ['PL-LB', 'Lubuskie'],
        ['PL-LD', 'Łódzkie'],
        ['PL-MA', 'Małopolskie'],
        ['PL-MZ', 'Mazowieckie'],
        ['PL-OP', 'Opolskie'],
        ['PL-PK', 'Podkarpackie'],
        ['PL-PD', 'Podlaskie'],
        ['PL-PM', 'Pomorskie'],
        ['PL-SL', 'Śląskie'],
        ['PL-SK', 'Świętokrzyskie'],
        ['PL-WN', 'Warmińsko-mazurskie'],
        ['PL-WP', 'Wielkopolskie'],
        ['PL-ZP', 'Zachodniopomorskie'],
    ],
    'Norway': [
        ['NO-42', 'Agder'],
        ['NO-34', 'Innlandet'],
        ['NO-15', 'Møre og Romsdal'],
        ['NO-18', 'Nordland'],
        ['NO-03', 'Oslo'],
        ['NO-11', 'Rogaland'],
        ['NO-54', 'Troms og Finnmark'], # / Romsa ja Finnmárku (se)
        ['NO-50', 'Trøndelag'],
        ['NO-38', 'Vestfold og Telemark'],
        ['NO-46', 'Vestland'],
        ['NO-30', 'Viken'],
        ['NO-22', 'Jan Mayen'],
        ['NO-21', 'Svalbard'],
        ['unknown', 'NOT SPECIFIED'],
        ['other', 'Outside mainland Norway'],  # CHECK ME!
    ],
    'Germany': [
        ['DE-BW', 'Baden-Württemberg'],
        ['DE-BY', 'Bayern'],
        ['DE-BE', 'Berlin'],
        ['DE-BB', 'Brandenburg'],
        ['DE-HB', 'Bremen'],
        ['DE-HH', 'Hamburg'],
        ['DE-HE', 'Hessen'],
        ['DE-MV', 'Mecklenburg-Vorpommern'],
        ['DE-NI', 'Niedersachsen'],
        ['DE-NW', 'Nordrhein-Westfalen'],
        ['DE-RP', 'Rheinland-Pfalz'],
        ['DE-SL', 'Saarland'],
        ['DE-SN', 'Sachsen'],
        ['DE-ST', 'Sachsen-Anhalt'],
        ['DE-SH', 'Schleswig Holstein'],
        ['DE-TH', 'Thüringen'],
        ['unknown', 'NOT SPECIFIED'],
        ['other', 'Repatriierte']
    ],
    'Sweden': [
        ['SE-K', 'Blekinge'],
        ['SE-W', 'Dalarna'],
        ['SE-I', 'Gotland'],
        ['SE-X', 'Gävleborg'],
        ['SE-N', 'Halland'],
        ['SE-Z', 'Jämtland'],
        ['SE-F', 'Jönköping'],
        ['SE-H', 'Kalmar'],
        ['SE-G', 'Kronoberg'],
        ['SE-BD', 'Norrbotten'],
        ['SE-M', 'Skåne'],
        ['SE-AB', 'Stockholm'],
        ['SE-D', 'Södermanland'],
        ['SE-C', 'Uppsala'],
        ['SE-S', 'Värmland'],
        ['SE-AC', 'Västerbotten'],
        ['SE-Y', 'Västernorrland'],
        ['SE-U', 'Västmanland'],
        ['SE-O', 'Västra Götaland'],
        ['SE-T', 'Örebro'],
        ['SE-E', 'Östergötland'],
    ],
}

for _k, _v in list(OVERRIDES.items()):
    OVERRIDES[_k] = dict(i[::-1] for i in _v)
    del _k, _v


class EUSubNationalData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/europe-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'eu_subnational'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'eu_subnational' / 'data',
             urls_dict={
                 'jrc-covid-19-regions-hxl.csv':
                     URL('https://raw.githubusercontent.com/ec-jrc/COVID-19/master/data-by-region/jrc-covid-19-all-days-by-regions.csv',
                         static_file=False),
             }
        )
        self.spdf = StrictDataPointsFactory(
            world_eu_mappings, MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.spdf()

        with self.get_file('jrc-covid-19-regions-hxl.csv',
                           include_revision=True) as f:
            first_line = True

            for item in csv.DictReader(f):
                if first_line:
                    first_line = False
                    continue
                print(item)

                date = self.convert_date(item['Date'])
                country = {
                    'NOT SPECIFIED': 'Unknown',
                }.get(item['CountryName'], item['CountryName']) \
                    .replace('Russian Fed.', 'Russian Federation') \
                    .replace('Czech Republic', '') \
                    .replace('Congo, Rep. Of', 'Congo') \
                    .replace('Myanmar, Union of', 'Myanmar') \
                    .replace('Guinea Bissau', 'Guinea-Bissau')

                # Ignore certain kinds of data, as it may not match with ISO 3166-2 etc
                if country in (
                    'Czechia',
                    'Czech Republic',
                    'Portugal',
                    'Spain',
                    'Italy',  # Has both admin-1 and admin-2 and would need to manually map to prevent confusion
                    'United Kingdom',

                    # Might be possible to fix these 2, but for now have specific datasources
                    'Switzerland',
                    'Greece',

                    'Whole Globe',
                    'Bonaire, Saint Eustatius and Saba',

                    'Australia',
                ):
                    continue

                # Get the name of the region
                region_child = item['Region']
                if region_child == 'NOT SPECIFIED':
                    region_child = 'unknown'
                elif country in OVERRIDES:
                    # HACK: Make sure using old version ISO 3166-2
                    #       which the Natural Earth geojson data uses
                    region_child = OVERRIDES[country][region_child]

                # Get the name of the country/schema
                if country == 'Finland':
                    schema = Schemas.FI_HEALTH_DISTRICT
                    country = 'FI'
                elif country == 'France':
                    # TODO: Support France regions (e.g. FR-IDF) as well as departments
                    # https://en.wikipedia.org/wiki/ISO_3166-2:FR
                    continue  # HACK!
                    #schema = Schemas.FR_REGION
                    #country = 'FR'
                elif country == 'Belgium':
                    continue
                    # schema = Schemas.BE_REGION
                    # country = 'FR'
                #elif country == 'Slovakia':
                #    continue
                    # schema = Schemas.SK_REGION
                    # country = 'SK'
                elif country == 'Albania':
                    # TODO: UPDATE THE GEOJSON!!! ===================================================================
                    continue
                elif country == 'Slovenia':
                    continue
                    # schema = Schemas.SI_STATISTICAL_REGION
                    # country = 'SI'
                elif country == 'Portugal':
                    continue
                elif region_child == country or not region_child:
                    region_child = country or region_child
                    country = None
                    schema = Schemas.ADMIN_0
                else:
                    schema = Schemas.ADMIN_1

                print(schema, country, region_child)

                for datatype, value in (
                    (DataTypes.TOTAL, item['CumulativePositive']),
                    (DataTypes.STATUS_DEATHS, item['CumulativeDeceased']),
                    (DataTypes.STATUS_RECOVERED, item['CumulativeRecovered']),
                    (DataTypes.STATUS_ACTIVE, item['CurrentlyPositive']),
                    (DataTypes.STATUS_HOSPITALIZED, item['Hospitalized']),
                    (DataTypes.STATUS_ICU, item['IntensiveCare'])
                ):
                    if value:
                        r.append(
                            region_schema=schema,
                            region_parent=country,
                            region_child=region_child,
                            datatype=datatype,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(EUSubNationalData().get_datapoints())
