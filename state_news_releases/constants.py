# Number of positive tests
DT_CASES = 0
DT_NEW_CASES = 1

# Number of case tests
DT_CASES_TESTED = 2

# Cases by region
DT_CASES_BY_REGION = 3
DT_NEW_CASES_BY_REGION = 4

# Patient status
DT_DEATHS = 5
DT_HOSPITALIZED = 6
DT_ICU = 7
DT_RECOVERED = 8

# Male/female cases
DT_MALE = 9
DT_FEMALE = 10
DT_NEW_MALE = 11
DT_NEW_FEMALE = 12

# Source of infection
DT_SOURCE_OF_INFECTION = 13
DT_NEW_SOURCE_OF_INFECTION = 14

# Age breakdowns
DT_AGE = 15  # Gender non-specific
DT_AGE_MALE = 16
DT_AGE_FEMALE = 17


def constant_to_name(x):
    for k, v in globals().items():
        if v == x:
            return k
