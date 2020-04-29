#============================================
# Schemas
#============================================

# Kinds of schemas
SCHEMA_STATEWIDE = 0  # Values for the whole state
SCHEMA_POSTCODE = 1
SCHEMA_LGA = 2  # Local Government Area
SCHEMA_HHS = 3  # Queensland
SCHEMA_LHD = 4  # NSW Local Health Districts
SCHEMA_THS = 5  # Tasmania Health Services

#============================================
# Datatypes
#============================================

# Case numbers
# (Age ranges are given as a separate value)
DT_CASES_NEW = 0
DT_CASES_NEW_MALE = 1
DT_CASES_NEW_FEMALE = 2
DT_CASES_TOTAL = 3
DT_CASES_TOTAL_MALE = 4
DT_CASES_TOTAL_FEMALE = 5

# Test numbers
DT_TESTS_TOTAL = 6
DT_TESTS_NEGATIVE = 7
DT_TESTS_POSITIVE = 8  # (Is this necessary?)

# Patient status
DT_STATUS_DEATH = 9
DT_STATUS_HOSPITALIZED = 10
DT_STATUS_ICU = 11
DT_STATUS_ICU_VENTILATORS = 12
DT_STATUS_RECOVERED = 13
DT_STATUS_ACTIVE = 14
DT_STATUS_UNKNOWN = 15

# Source of infection
DT_SOURCE_OVERSEAS = 16  # Overseas, counted separately
DT_SOURCE_CRUISE_SHIP = 17  # Overseas, included in DT_SOURCE_OVERSEAS
DT_SOURCE_INTERSTATE = 18  # Local-transmission from interstate, counted separately
DT_SOURCE_CONFIRMED = 19  # Local-transmission from confirmed cases, counted separately
DT_SOURCE_COMMUNITY = 20  # Local-unknown community transmission, counted separately
DT_SOURCE_UNDER_INVESTIGATION = 21  # "other"


def schema_to_name(x):
    for k, v in globals().items():
        if k.startswith('SCHEMA_') and v == x:
            return k


def constant_to_name(x):
    for k, v in globals().items():
        if k.startswith('DT_') and v == x:
            return k
