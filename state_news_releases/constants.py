# possible datatypes
DT_CASES_TESTED = 0
DT_NEW_CASES = 1
DT_CASES_BY_REGION = 2
DT_NEW_CASES_BY_REGION = 3
DT_CASES = 3
DT_FATALITIES = 4
DT_HOSPITALIZED = 5
DT_RECOVERED = 6


def constant_to_name(x):
    for k, v in globals().items():
        if v == x:
            return k
