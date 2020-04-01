# possible datatypes
DT_CASES = 0
DT_NEW_CASES = 1
DT_CASES_TESTED = 2

DT_CASES_BY_REGION = 3
DT_NEW_CASES_BY_REGION = 4

DT_DEATHS = 5
DT_HOSPITALIZED = 6
DT_ICU = 7
DT_RECOVERED = 8

DT_MALE = 9
DT_FEMALE = 10

DT_SOURCE_OF_INFECTION = 11
DT_NEW_SOURCE_OF_INFECTION = 12


def constant_to_name(x):
    for k, v in globals().items():
        if v == x:
            return k
