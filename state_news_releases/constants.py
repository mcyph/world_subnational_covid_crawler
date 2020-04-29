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

# DT_POPULATION???

# Case numbers+patient status
# (Age ranges are given as a separate value)
DT_CASES_NEW = 0
DT_CASES_NEW_MALE = 1
DT_CASES_NEW_FEMALE = 2
DT_CASES_TOTAL = 3
DT_CASES_TOTAL_MALE = 4
DT_CASES_TOTAL_FEMALE = 5
DT_CASES_DEATHS = 6
DT_CASES_HOSPITALIZED = 7
DT_CASES_ICU = 8
DT_CASES_ICU_VENTILATORS = 9
DT_CASES_RECOVERED = 10
DT_CASES_ACTIVE = 11
DT_CASES_UNKNOWN = 12

# Test numbers
DT_TESTS_TOTAL = 13
DT_TESTS_NEGATIVE = 14
DT_TESTS_POSITIVE = 15  # (Is this necessary?)

# Source of infection
DT_SOURCE_OVERSEAS = 16  # Overseas, counted separately
DT_SOURCE_CRUISE_SHIP = 17  # Overseas, included in DT_SOURCE_OVERSEAS
DT_SOURCE_INTERSTATE = 18  # Local-transmission from interstate, counted separately
DT_SOURCE_CONFIRMED = 19  # Local-transmission from confirmed cases, counted separately
DT_SOURCE_COMMUNITY = 20  # Local-unknown community transmission, counted separately
DT_SOURCE_UNDER_INVESTIGATION = 21  # "other"

# State-specific
# SA
#DT_EXPIATIONS_TOTAL
#DT_EXPIATIONS_FINES
#DT_EXPIATIONS_CAUTIONS
#DT_EXPIATIONS_PERSON
#DT_EXPIATIONS_BUSINESS
#DT_EMERGENCY_DIRECTION_COMPLIANCE_PERSONAL_CHECKS
#DT_EMERGENCY_DIRECTION_COMPLIANCE_PERSONAL_COMPLIANT
#DT_EMERGENCY_DIRECTION_COMPLIANCE_BUSINESS_CHECKS
#DT_EMERGENCY_DIRECTION_COMPLIANCE_BUSINESS_COMPLIANT
#DT_TRAVELLERS_TOTAL
#DT_TRAVELLERS_ESSENTIAL

# NT
#DT_FORCED_QUARANTINE
#DT_INFRINGEMENTS_ISSUED
#DT_COMPLIANCE_CHECKS_COMPLETED
#DT_ENTERED_BY_ROAD
#DT_ENTERED_BY_TRAIN
#DT_ENTERED_BY_PLANE
#DT_ENTERED_BY_SEA

# QLD
#DT_SELF_QUARANTINE_NOTICES_TOTAL
#DT_SELF_QUARANTINE_NOTICES_ACTIVE
#DT_SELF_QUARANTINE_NOTICES_COMPLETED


def schema_to_name(x):
    for k, v in globals().items():
        if k.startswith('SCHEMA_') and v == x:
            return k


def constant_to_name(x):
    for k, v in globals().items():
        if k.startswith('DT_') and v == x:
            return k
