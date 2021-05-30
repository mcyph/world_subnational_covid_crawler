from enum import Enum


#============================================
# Schemas
#============================================


class Schemas(str, Enum):
    # Kinds of schemas
    ADMIN_0 = 'admin_0'
    ADMIN_1 = 'admin_1'  # Values for the whole state
    OCHA_ADMIN_1 = 'ocha_admin_1'
    POSTCODE = 'postcode'
    LGA = 'lga'  # Local Government Area
    HHS = 'hhs'  # Queensland
    LHD = 'lhd'  # NSW Local Health Districts
    THS = 'ths'  # Tasmania Health Services
    SA3 = 'sa3'  # SA3 for ACT
    
    # https://covid-19-coronavirus.tools/
    BD_DISTRICT = 'bd_district'
    BR_CITY = 'br_city'
    CN_CITY = 'cn_city'
    CO_MUNICIPALITY = 'co_municipality'
    #DE_AGS = 'de_ags'
    #ES_MADRID_MUNICIPALITY = 'es_madrid_municipality
    #FR_DEPARTMENT = 'fr_department'
    FR_OVERSEAS_COLLECTIVITY = 'fr_overseas_collectivity'   # TODO: CONSIDER WHETHER TO REMOVE ME!!!
    IN_DISTRICT = 'in_district'
    IT_PROVINCE = 'it_province'
    JP_CITY = 'jp_city'
    MY_DISTRICT = 'my_district'
    NZ_DHB = 'nz_dhb'  # District Health Board
    TH_DISTRICT = 'th_district'
    UK_AREA = 'uk_area'   # TODO: Split into different countries!!! ==========================================
    US_COUNTY = 'us_county'
    PS_PROVINCE = 'ps_province'
    CR_CANTON = 'cr_canton'
    CU_MUNICIPALITY = 'cu_municipality'
    CA_HEALTH_REGION = 'ca_health_region'
    #LK_DISTRICT = 'lk_district'
    #ES_AUTONOMOUS_COMMUNITY = 'es_autonomous_community'
    NP_DISTRICT = 'np_district'
    PT_MUNICIPALITY = 'pt_municipality'
    CZ_OKRES = 'cz_okres'
    FI_HEALTH_DISTRICT = 'fi_health_district'
    
    TR_NUTS1 = 'tr_nuts1'
    #NUTS_2 = 'nuts_2'
    #NUTS_3 = 'nuts_3'
    
    DE_KREIS = 'de_kreis'
    LT_MUNICIPALITY = 'lt_municipality'
    IL_MUNICIPALITY = 'il_municipality'
    HK_DISTRICT = 'hk_district'
    ES_PROVINCE = 'es_province'


#============================================
# Datatypes
#============================================


class DataTypes(str, Enum):
    # POPULATION???
    
    # Case numbers+patient status
    # (Age ranges are given as a separate value)
    NEW = 'new'
    NEW_MALE = 'new_male'
    NEW_FEMALE = 'new_female'
    TOTAL = 'total'
    TOTAL_MALE = 'total_male'
    TOTAL_FEMALE = 'total_female'
    
    CONFIRMED = 'confirmed'
    PROBABLE = 'probable'
    CONFIRMED_NEW = 'confirmed_new'
    PROBABLE_NEW = 'probable_new'
    
    # Totals by status
    STATUS_DEATHS = 'status_deaths'
    STATUS_HOSPITALIZED = 'status_hospitalized'
    STATUS_HOSPITALIZED_RUNNINGTOTAL = 'status_hospitalized_runningtotal'
    STATUS_ICU = 'status_icu'
    STATUS_ICU_VENTILATORS = 'status_icu_ventilators'
    STATUS_ICU_RUNNINGTOTAL = 'status_icu_runningtotal'
    STATUS_ICU_VENTILATORS_RUNNINGTOTAL = 'status_icu_ventilators_runningtotal'
    STATUS_VACCINATED = 'status_vaccinated'
    STATUS_RECOVERED = 'status_recovered'
    STATUS_ACTIVE = 'status_active'
    STATUS_UNKNOWN = 'status_unknown'
    
    STATUS_DEATHS_NEW = 'status_deaths_new'
    STATUS_HOSPITALIZED_NEW = 'status_hospitalized_new'
    STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW = 'status_hospitalized_runningtotal_new'
    STATUS_DISCHARGED_DEATHS = 'status_discharged_deaths'
    STATUS_ICU_NEW = 'status_icu_new'
    STATUS_ICU_VENTILATORS_NEW = 'status_icu_ventilators_new'
    STATUS_ICU_RUNNINGTOTAL_NEW = 'status_icu_runningtotal_new'
    STATUS_ICU_VENTILATORS_RUNNINGTOTAL_NEW = 'status_icu_ventilators_runningtotal_new'
    STATUS_RECOVERED_NEW = 'status_recovered_new'
    STATUS_ACTIVE_NEW = 'status_active_new'
    STATUS_UNKNOWN_NEW = 'status_unknown_new'

    STATUS_ACTIVE_MALE = 'status_active_male'
    STATUS_ACTIVE_FEMALE = 'status_active_female'
    
    # Totals by source of infection (totals)
    SOURCE_OVERSEAS = 'source_overseas'  # Overseas, counted separately
    SOURCE_CRUISE_SHIP = 'source_cruise_ship'  # Overseas, included in SOURCE_OVERSEAS
    SOURCE_INTERSTATE = 'source_interstate'  # Local-transmission from interstate, counted separately
    SOURCE_CONFIRMED = 'source_confirmed'  # Local-transmission from confirmed cases, counted separately
    SOURCE_COMMUNITY = 'source_community'  # Local-unknown community transmission, counted separately
    SOURCE_UNDER_INVESTIGATION = 'source_under_investigation'  # "other"
    SOURCE_DOMESTIC = 'source_domestic'  # For in-country which may or may not be community transmission (New Zealand data)

    # active
    SOURCE_OVERSEAS_ACTIVE = 'source_overseas_active'
    SOURCE_CRUISE_SHIP_ACTIVE = 'source_cruise_ship_active'
    SOURCE_INTERSTATE_ACTIVE = 'source_interstate_active'
    SOURCE_CONFIRMED_ACTIVE = 'source_confirmed_active'
    SOURCE_COMMUNITY_ACTIVE = 'source_community_active'
    SOURCE_UNDER_INVESTIGATION_ACTIVE = 'source_under_investigation_active'
    SOURCE_DOMESTIC_ACTIVE = 'source_domestic_active'
    
    # Test numbers
    TESTS_TOTAL = 'tests_total'
    TESTS_NEGATIVE = 'tests_negative'
    TESTS_POSITIVE = 'tests_positive'  # (Is this necessary?)
    TESTS_NEW = 'tests_new'

    AGE_CARE_TOTAL = 'age_care_total'
    AGE_CARE_MALE = 'age_care_male'
    AGE_CARE_FEMALE = 'age_care_female'

    AGE_CARE_NEW = 'age_care_new'
    AGE_CARE_MALE_NEW = 'age_care_male_new'
    AGE_CARE_FEMALE_NEW = 'age_care_female_new'
    
    FACEBOOK_COVID_SYMPTOMS = 'facebook_covid_symptoms'
    FACEBOOK_FLU_SYMPTOMS = 'facebook_flu_symptoms'

    GOOGLE_MOBILITY_RETAIL_RECREATION = 'google_mobility_retail_recreation'
    GOOGLE_MOBILITY_SUPERMARKET_PHARMACY = 'google_mobility_supermarket_pharmacy'
    GOOGLE_MOBILITY_PARKS = 'google_mobility_parks'
    GOOGLE_MOBILITY_PUBLIC_TRANSPORT = 'google_mobility_public_transport'
    GOOGLE_MOBILITY_WORKPLACES = 'google_mobility_workplaces'
    GOOGLE_MOBILITY_RESIDENTIAL = 'google_mobility_residential'


if __name__ == '__main__':
    import json
    print(json.dumps([DataTypes.STATUS_ACTIVE]))
    print(DataTypes("status_active"))
    print("%s" % str(DataTypes.STATUS_ACTIVE))

    D = {}
    D[DataTypes.STATUS_ACTIVE] = "test"
    print(D['status_active'])
