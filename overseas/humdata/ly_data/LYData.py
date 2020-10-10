import csv

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir


class LYData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/' \
                 'libya-coronavirus-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ly_hdx_humdata'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'ly' / 'data',
             urls_dict={
                 'ly_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/'
                     '2PACX-1vQQWJZmGZJfUm22CPWoeW6rSS7Xh4K54r4A8RlN214ZCIPBUBOug3UbxFPrbiT3FQic6HS8wGdUhv3f/'
                     'pub?output=csv',
                     static_file=False
                 )
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'ly', 'اجدابيا'): None, # Ajdabiya, Al Wahat
                ('admin_1', 'ly', 'البريقة'): None, # Brega, Al Wahat
                ('admin_1', 'ly', 'البيضاء'): None, # Bayda, Jabal al Akhdar
                ('admin_1', 'ly', 'الجفارة'): None, # Jafara
                ('admin_1', 'ly', 'الجميل'): None, # Aljmail, Nuqat al Khams
                ('admin_1', 'ly', 'الخمس'): None, # Al-Khums, Murqub
                ('admin_1', 'ly', 'الرجبان'): None, # Alrujban, ???
                ('admin_1', 'ly', 'الرحيبات'): None, # Alruhaibat, ???
                ('admin_1', 'ly', 'الرياينة'): None, # Alriyayna, ???
                ('admin_1', 'ly', 'الزاوية'): None, # Az-Zāwiyah, ???
                ('admin_1', 'ly', 'الزنتان'): None, # Alzintan, Jabal al Gharbi
                ('admin_1', 'ly', 'العجيلات'): None, # Ajaylat, Nuqat al Khams
                ('admin_1', 'ly', 'العزيزية'): None, # ʽAziziya, Jafara
                ('admin_1', 'ly', 'القلعة'): None,
                ('admin_1', 'ly', 'الكفرة'): None, # Kufra District
                ('admin_1', 'ly', 'المحروقة'): None,
                ('admin_1', 'ly', 'المرج'): None, # Marj, Marj
                ('admin_1', 'ly', 'بني وليد'): None, # Bani Walid, Misrata District
                ('admin_1', 'ly', 'جادو'): None,
                ('admin_1', 'ly', 'جنزور'): None, # Janzur, Janzour/Greater Tripoli???
                ('admin_1', 'ly', 'درنة'): None, # Derna, Derna
                ('admin_1', 'ly', 'رقدالين'): None,
                ('admin_1', 'ly', 'زلطن'): None,
                ('admin_1', 'ly', 'زليتن'): None,
                ('admin_1', 'ly', 'زوارة'): None,
                ('admin_1', 'ly', 'سبها'): None,
                ('admin_1', 'ly', 'سرت'): None,
                ('admin_1', 'ly', 'صبراتة'): None,
                ('admin_1', 'ly', 'صرمان'): None,
                ('admin_1', 'ly', 'طبرق'): None,
                ('admin_1', 'ly', 'طرابلس'): None,
                ('admin_1', 'ly', 'غدامس'): None,
                ('admin_1', 'ly', 'غريان'): None,
                ('admin_1', 'ly', 'قصر الاخيار'): None,
                ('admin_1', 'ly', 'قصر بن غشير'): None,
                ('admin_1', 'ly', 'مزدة'): None,
                ('admin_1', 'ly', 'مسلاتة'): None,
                ('admin_1', 'ly', 'مصراتة'): None,
                ('admin_1', 'ly', 'نالوت'): None,
                ('admin_1', 'ly', 'هراوة'): None,
                ('admin_1', 'ly', 'وادي الشاطيء'): None,
                ('admin_1', 'ly', 'يفرن'): None,
                ('admin_1', 'ly', 'سوسة'): None,
                ('admin_1', 'ly', 'تيجي'): None,
                ('admin_1', 'ly', 'امساعد'): None,
                ('admin_1', 'ly', 'الزهرة'): None,
                ('admin_1', 'ly', 'السبيعة'): None,
                ('admin_1', 'ly', 'تندميرة'): None,
                ('admin_1', 'ly', 'بن جواد'): None,
                ('admin_1', 'ly', 'الأبيار'): None,
                ('admin_1', 'ly', 'كاباو'): None,
                ('admin_1', 'ly', 'الجفرة'): None,
                ('admin_1', 'ly', 'ككلة'): None,
                ('admin_1', 'ly', 'الشويرف'): None,
                ('admin_1', 'ly', 'ترهونة'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()

        # Governorate,Confirmed Cases,Recoveries,Deaths,Active,Date
        #
        # #adm2+name,#affected+infected+confirmed,#affected+infected+recovered,
        # #affected+infected+dead,#affected+infected+active,#date
        #
        # Benghazi,4,4,,,2020-05-12
        # Misurata,10,10,,,2020-05-12
        # Sorman,1,1,,,2020-05-12
        # Tripoli,49,13,3,33,2020-05-12

        first_item = True
        f = self.get_file('ly_data.csv',
                          include_revision=True)

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            #print(item)
            date = self.convert_date(item['Date'], formats=('%m/%d/%Y',))
            region_child = item['Location'].title() # Location was Governorate

            if item['Confirmed']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='LY',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(item['Confirmed'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Deaths']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='LY',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['Deaths'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Recoveries']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='LY',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(item['Recoveries'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Active']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='LY',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(item['Active'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Test Samples']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='LY',
                    region_child=region_child,
                    datatype=DataTypes.TESTS_TOTAL,
                    value=int(item['Test Samples'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = LYData()
    inst.sdpf.print_mappings()
    datapoints = inst.get_datapoints()
    #pprint()
