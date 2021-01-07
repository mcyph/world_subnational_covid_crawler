from os import environ
import pygsheets
import pandas as pd
from geopy.geocoders import MapBox

from _utility.get_package_dir import get_package_dir
from case_locations.nsw.get_nsw_case_locations import get_nsw_case_locations
#from case_locations.vic.get_vic_case_locations import get_vic_case_locations
from case_locations.vic.get_vic_case_locations_2 import get_vic_case_locations
from case_locations._base_classes.datatypes import VenueLocation


def crawl_case_locations():
    out = []
    out.extend(get_nsw_case_locations())
    out.extend(get_vic_case_locations())
    return out


def df_to_dicts(df):
    """

    """
    return [dict(zip(df.columns, i)) for i in df.values.tolist()]


GEOLOCATOR = [None]


def dicts_to_df(geocoords_by_key, dicts):
    """

    """
    def process_dict(d):
        if isinstance(d, VenueLocation):
            out = d.to_dict()
            vl = d
        else:
            if 'name' in d:
                del d['name']
            if 'coor' in d:
                d['long'], d['lat'] = d['coor']
                del d['coor']
            out = d.copy()
            vl = VenueLocation.from_dict(d)

        if not out['long'] and vl.get_geocoord_key() in geocoords_by_key:
            out['long'], out['lat'] = geocoords_by_key[vl.get_geocoord_key()]
        elif 'trains' in out['venue'].lower() or 'v/line' in out['venue'].lower():
            # Need to add public transport lines separately!
            pass
        elif not out['long']:
            if not GEOLOCATOR[0]:
                GEOLOCATOR[0] = MapBox(
                    api_key=environ['MAPBOX_KEY'],
                    user_agent="https://covid-19-au.com"
                )
            try:
                location = GEOLOCATOR[0].geocode(out['venue']+', '+out['area']+', '+out['state'])
                print(out, location)
                if location:
                    out['long'] = location.longitude
                    out['lat'] = location.latitude
            except:
                # Make sure it doesn't keep trying to get the lat/long
                # when the service didn't find the location!
                import traceback
                traceback.print_exc()
                out['long'] = '!error'
                out['lat'] = '!error'
        return out

    df = pd.DataFrame(
        columns=['state', 'area', 'venue', 'long', 'lat',
                 'type', 'date', 'time', 'description'],

        data=[process_dict(i) for i in dicts]
    )
    #df['long'] = df['long'].astype('float')
    #df['lat'] = df['lat'].astype('float')
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    return df


def get_geocoords_by_key(venue_locations):
    """

    """
    def to_venue_location(i):
        if not isinstance(i, VenueLocation):
            return VenueLocation.from_dict(i)
        return i

    venue_locations = [to_venue_location(i) for i in venue_locations]
    return {i.get_geocoord_key(): (i.long, i.lat)
            for i in venue_locations
            if i.long and i.lat}


def get_worksheet():
    """

    """
    gc = pygsheets.authorize(
        service_file=str(get_package_dir() / 'case_locations' / 'credentials.json')
    )
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/'
        '1ddw3GqI4RsrphdjJcYX-llnQ-JTV_q2atOr1UToLbw0/edit#gid=0'
    )
    wk1 = sh[0]
    return wk1


def update_spreadsheet(wk1):
    # Get the previous data from the spreadsheet
    old_df = wk1.get_as_df(has_header=False)
    new_header = old_df.iloc[0]  # grab the first row for the header
    old_df = old_df[1:]  # take the data less the header row
    old_df.columns = new_header  # set the header row as the df header

    #print("OLD:", old_df.columns, old_df)
    old_dicts = df_to_dicts(old_df)
    #print(old_dicts)
    geocoords_by_key = get_geocoords_by_key(old_dicts)

    new_dicts = crawl_case_locations()
    new_df = dicts_to_df(geocoords_by_key, new_dicts)
    #print(new_df)
    new_df = new_df.sort_values(by=['date', 'state', 'area', 'venue'],
                                ascending=[False, True, True, True])

    wk1.set_dataframe(new_df, (1, 1), nan='')


def get_worksheet_data_as_dicts(remove_no_geoloc=True):
    """

    """
    wk1 = get_worksheet()
    r = df_to_dicts(wk1.get_as_df())
    if remove_no_geoloc:
        out = []
        for i in r:
            if not i['lat']:
                continue
            elif i['lat'] == '!error':
                continue
            out.append(i)
        r = out
    return r


if __name__ == '__main__':
    # Load the worksheet from Google Sheets
    wk1 = get_worksheet()

    if False:
        # Migrate from the previous format
        import json
        PATH = '/home/david/containers/dev/covid-19-au.github.io/src/data/mapdataCon.json'

        with open(PATH, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        df = dicts_to_df(data)
    else:
        update_spreadsheet(wk1)
