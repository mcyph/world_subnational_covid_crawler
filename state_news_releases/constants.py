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
DT_CASES_BY_LGA = 8  # Compatibility for Queensland HHS
DT_CASES_BY_OVERSEAS_ACQUIRED = 9
DT_CASES_BY_CONTACT_KNOWN = 10  # Locally acquired
DT_CASES_BY_NO_KNOWN_CONTACT = 11  # Locally acquired
DT_CASES_BY_INTERSTATE = 12
DT_CASES_BY_UNDER_INVESTIGATION = 13
DT_NEW_CASES_BY_REGION = 14
DT_NEW_CASES_BY_LHA = 15

# Patient status
# (includes Deaths, Hospitalized, ICU,
#  ICU Ventilators, Recovered as "name")
DT_PATIENT_STATUS = 16

# Male/female cases
DT_MALE = 17
DT_FEMALE = 18
DT_NEW_MALE = 19
DT_NEW_FEMALE = 20

# Source of infection
DT_SOURCE_OF_INFECTION = 21
DT_NEW_SOURCE_OF_INFECTION = 22

# Age breakdowns
DT_AGE = 23  # Gender non-specific
DT_AGE_MALE = 24
DT_AGE_FEMALE = 25


def constant_to_name(x):
    for k, v in globals().items():
        if v == x:
            return k
