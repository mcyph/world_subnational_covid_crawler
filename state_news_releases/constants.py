# Number of positive tests
DT_CASES = 0
DT_NEW_CASES = 1

# Number of case tests
DT_CASES_TESTED = 2

# Cases by region
DT_CASES_BY_REGION = 3
DT_NEW_CASES_BY_REGION = 4

# Patient status
DT_PATIENT_STATUS = 5
#DT_DEATHS = 5
#DT_HOSPITALIZED = 6
#DT_ICU = 7
#DT_ICU_VENTILATORS = 8
#DT_RECOVERED = 9

# Male/female cases
DT_MALE = 6
DT_FEMALE = 7
DT_NEW_MALE = 8
DT_NEW_FEMALE = 9

# Source of infection
DT_SOURCE_OF_INFECTION = 10
DT_NEW_SOURCE_OF_INFECTION = 11

# Age breakdowns
DT_AGE = 12  # Gender non-specific
DT_AGE_MALE = 13
DT_AGE_FEMALE = 14


def constant_to_name(x):
    for k, v in globals().items():
        if v == x:
            return k
