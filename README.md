# Introduction

This repo contains a collection of scrapers I wrote for both Australian and 
international COVID-19 data. It also includes a basic web interface for 
monitoring its status, and parsing for statistics which can be overlayed 
with COVID-19 data, such as economic and other data from the Australian 
Bureau of Statistics.  

It mainly differs from other similar projects because it not only provides national 
data, it also crawls data on sub-national and sub-state/province/territory 
levels where it is available. It also includes statistics on age group breakdowns 
and infection sources in many cases. The outputted data is updated periodically and 
can be obtained from https://github.com/mcyph/global_subnational_covid_data.
There are plans to make it update automatically soon.

It was intended to automatically obtain statistics related to COVID-19 for the 
[COVID-19 Case Tracker Australia](https://covid-19-au.com/) website which was 
started by Dr. Chunyang Chen and a group of volunteers at Monash and other 
Australian universities.

* state_news_releases/ will get various statistics from Australian state government 
  news releases. It obtains data on a state and sub-state level.
  
  * ACT: Basic statistics from press releases. Regional and infection 
         source statistics from the ACT PowerBI dashboard. 
  * New South Wales: Regional (LGA, LHS, postcode) and statewide statistics 
         from government press releases and open data.
  * Northern Territory: Basic statewide statistics only.
  * South Australia: Regional (LGA total and active) and statewide statistics. 
  * Tasmania: Regional (LGA) and statewide statistics from news reports. 
         Note LGA can be more than a week old due to these figures only being 
         updated periodically by the Tasmanian government.
  * Victoria: Basic statistics from press releases and daily statistics pages.
         regional LGA (totals and active cases) and infection 
         source statistics from the ACT PowerBI dashboard. 
  * Western Australia: Basic statistics from press releases. 
         Regional statistics (LGA) and infection source are available 
         from the dashboard data.

* db/ [....]

* datatypes/ [.....]

* geojson_data/ provides processing and normalization of various different 
  GeoJSON data files to be used with the covid-19-au case tracker.

* hospitals/get_hospitals.py gets COVID-19 hospital/clinic information 
  from the state websites. As of 29 March the WA data needs to be updated 
  to a different URL.
  
* web_interface/ [.....]

# Schema information

# Kinds of schemas
SCHEMA_ADMIN_0 = 0
SCHEMA_ADMIN_1 = 1  # Values for the whole state
SCHEMA_POSTCODE = 2
SCHEMA_LGA = 3  # Local Government Area
SCHEMA_HHS = 4  # Queensland
SCHEMA_LHD = 5  # NSW Local Health Districts
SCHEMA_THS = 6  # Tasmania Health Services
SCHEMA_SA3 = 7  # SA3 for ACT

SCHEMA_BD_DISTRICT = 8
SCHEMA_BR_CITY = 9
SCHEMA_CO_MUNICIPALITY = 10
SCHEMA_DE_AGS = 11
SCHEMA_ES_MADRID_MUNICIPALITY = 12
SCHEMA_FR_DEPARTMENT = 13
SCHEMA_FR_OVERSEAS_COLLECTIVITY = 14   # TODO: CONSIDER WHETHER TO REMOVE ME!!!
SCHEMA_IN_DISTRICT = 15
SCHEMA_IT_PROVINCE = 16
SCHEMA_JP_CITY = 17
SCHEMA_MY_DISTRICT = 18
SCHEMA_NZ_DHB = 19  # District Health Board
SCHEMA_TH_DISTRICT = 20
SCHEMA_UK_AREA = 21   # TODO: Split into different countries!!! ==========================================
SCHEMA_US_COUNTY = 22

# DT_POPULATION???

# Case numbers+patient status
# (Age ranges are given as a separate value)
DT_NEW = 0
DT_NEW_MALE = 1
DT_NEW_FEMALE = 2
DT_TOTAL = 3
DT_TOTAL_MALE = 4
DT_TOTAL_FEMALE = 5

DT_CONFIRMED = 8
DT_PROBABLE = 11
DT_CONFIRMED_NEW = 14
DT_PROBABLE_NEW = 17

# Totals by status
DT_STATUS_DEATHS = 20
DT_STATUS_HOSPITALIZED = 21
DT_STATUS_HOSPITALIZED_RUNNINGTOTAL = 22
DT_STATUS_ICU = 23
DT_STATUS_ICU_VENTILATORS = 24
DT_STATUS_ICU_RUNNINGTOTAL = 25
DT_STATUS_ICU_VENTILATORS_RUNNINGTOTAL = 26
DT_STATUS_RECOVERED = 27
DT_STATUS_ACTIVE = 30
DT_STATUS_UNKNOWN = 33

DT_STATUS_DEATHS_NEW = 34
DT_STATUS_HOSPITALIZED_NEW = 35
DT_STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW = 36
DT_STATUS_ICU_NEW = 37
DT_STATUS_ICU_VENTILATORS_NEW = 38
DT_STATUS_ICU_RUNNINGTOTAL_NEW = 39
DT_STATUS_ICU_VENTILATORS_RUNNINGTOTAL_NEW = 40
DT_STATUS_RECOVERED_NEW = 41
DT_STATUS_ACTIVE_NEW = 42
DT_STATUS_UNKNOWN_NEW = 43

# Totals by source of infection
DT_SOURCE_OVERSEAS = 44  # Overseas, counted separately
DT_SOURCE_CRUISE_SHIP = 45  # Overseas, included in DT_SOURCE_OVERSEAS
DT_SOURCE_INTERSTATE = 46  # Local-transmission from interstate, counted separately
DT_SOURCE_CONFIRMED = 47  # Local-transmission from confirmed cases, counted separately
DT_SOURCE_COMMUNITY = 48  # Local-unknown community transmission, counted separately
DT_SOURCE_UNDER_INVESTIGATION = 49  # "other"
DT_SOURCE_DOMESTIC = 50  # For in-country which may or may not be community transmission (New Zealand data)

# Test numbers
DT_TESTS_TOTAL = 58
DT_TESTS_NEGATIVE = 61
DT_TESTS_POSITIVE = 62  # (Is this necessary?)
DT_TESTS_NEW = 63