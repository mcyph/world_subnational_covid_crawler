# Number of positive tests
DT_CASES = 0
DT_NEW_CASES = 1

# Number of case tests
DT_CASES_TESTED = 2

# Cases by region
DT_CASES_BY_REGION = 3
DT_CASES_BY_REGION_ACTIVE = 4
DT_CASES_BY_REGION_RECOVERED = 5
DT_CASES_BY_REGION_DEATHS = 6
DT_CASES_BY_LHA = 7
DT_NEW_CASES_BY_REGION = 8
DT_NEW_CASES_BY_LHA = 9

# Patient status
# (includes Deaths, Hospitalized, ICU,
#  ICU Ventilators, Recovered as "name")
DT_PATIENT_STATUS = 10

# Male/female cases
DT_MALE = 11
DT_FEMALE = 12
DT_NEW_MALE = 13
DT_NEW_FEMALE = 14

# Source of infection
DT_SOURCE_OF_INFECTION = 15
DT_NEW_SOURCE_OF_INFECTION = 16

# Age breakdowns
DT_AGE = 17  # Gender non-specific
DT_AGE_MALE = 18
DT_AGE_FEMALE = 19


def constant_to_name(x):
    for k, v in globals().items():
        if v == x:
            return k
