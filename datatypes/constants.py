#============================================
# Schemas
#============================================

# Kinds of schemas
SCHEMA_ADMIN_0 = 0
SCHEMA_ADMIN_1 = 1  # Values for the whole state
SCHEMA_POSTCODE = 2
SCHEMA_LGA = 3  # Local Government Area
SCHEMA_HHS = 4  # Queensland
SCHEMA_LHD = 5  # NSW Local Health Districts
SCHEMA_THS = 6  # Tasmania Health Services
SCHEMA_SA3 = 7  # SA3 for ACT

# https://covid-19-coronavirus.tools/
SCHEMA_BD_DISTRICT = 8
SCHEMA_BR_CITY = 9
SCHEMA_CO_MUNICIPALITY = 10
#SCHEMA_DE_AGS = 11
#SCHEMA_ES_MADRID_MUNICIPALITY = 12
#SCHEMA_FR_DEPARTMENT = 13
SCHEMA_FR_OVERSEAS_COLLECTIVITY = 14   # TODO: CONSIDER WHETHER TO REMOVE ME!!!
SCHEMA_IN_DISTRICT = 15
SCHEMA_IT_PROVINCE = 16
SCHEMA_JP_CITY = 17
SCHEMA_MY_DISTRICT = 18
SCHEMA_NZ_DHB = 19  # District Health Board
SCHEMA_TH_DISTRICT = 20
SCHEMA_UK_AREA = 21   # TODO: Split into different countries!!! ==========================================
SCHEMA_US_COUNTY = 22
SCHEMA_PS_PROVINCE = 23
SCHEMA_CR_CANTON = 24
SCHEMA_CU_MUNICIPALITY = 25
SCHEMA_CA_HEALTH_REGION = 26
#SCHEMA_LK_DISTRICT = 27
#SCHEMA_ES_AUTONOMOUS_COMMUNITY = 28
SCHEMA_NP_DISTRICT = 29
SCHEMA_PT_MUNICIPALITY = 30
SCHEMA_CZ_OKRES = 31
SCHEMA_FI_HEALTH_DISTRICT = 32

SCHEMA_TR_NUTS1 = 33
#SCHEMA_NUTS_2 = 34
#SCHEMA_NUTS_3 = 35

SCHEMA_DE_KREIS = 36
SCHEMA_LT_MUNICIPALITY = 37
SCHEMA_IL_MUNICIPALITY = 38
SCHEMA_HK_DISTRICT = 39

#============================================
# Datatypes
#============================================

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


def schema_to_name(x):
    for k, v in globals().items():
        if k.startswith('SCHEMA_') and v == x:
            return k[7:].lower()


def datatype_to_name(x):
    for k, v in globals().items():
        if k.startswith('DT_') and v == x:
            return k[3:].lower()


def name_to_schema(x):
    return globals()['SCHEMA_'+x.upper()]


def name_to_datatype(x):
    return globals()['DT_' + x.upper()]


def get_schemas():
    r = []
    for k, v in globals().items():
        if k.startswith('SCHEMA_'):
            r.append(v)
    return r
