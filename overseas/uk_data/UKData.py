import csv

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_UK_AREA, SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    DT_TOTAL, DT_TESTS_TOTAL,
    DT_STATUS_DEATHS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)

place_map = dict([i.split('\t')[::-1] for i in """
GB-ABE	Aberdeen City
GB-ABD	Aberdeenshire
GB-ANS	Angus
GB-ANN	Antrim and Newtownabbey
GB-AND	Ards and North Down
GB-AND	North Down and Ards
GB-AGB	Argyll and Bute
GB-ABC	Armagh City, Banbridge and Craigavon
GB-ABC	Armagh, Banbridge and Craigavon
GB-BDG	Barking and Dagenham
GB-BNE	Barnet
GB-BNS	Barnsley
GB-BAS	Bath and North East Somerset
GB-BDF	Bedford
GB-BFS	Belfast
GB-BEX	Bexley
GB-BIR	Birmingham
GB-BBD	Blackburn with Darwen
GB-BPL	Blackpool
GB-BGW	Blaenau Gwent
GB-BOL	Bolton
GB-BMH	Bournemouth
GB-BRC	Bracknell Forest
GB-BRD	Bradford
GB-BEN	Brent
GB-BGE	Bridgend
GB-BNH	Brighton and Hove
GB-BST	Bristol, City of
GB-BRY	Bromley
GB-BKM	Buckinghamshire
GB-BUR	Bury
GB-CAY	Caerphilly
GB-CLD	Calderdale
GB-CAM	Cambridgeshire
GB-CMD	Camden
GB-CRF	Cardiff
GB-CMN	Carmarthenshire
GB-CCG	Causeway Coast and Glens
GB-CBF	Central Bedfordshire
GB-CGN	Ceredigion
GB-CHE	Cheshire East
GB-CHW	Cheshire West and Chester
GB-CLK	Clackmannanshire
GB-CWY	Conwy
GB-CON	Cornwall
GB-CON	Cornwall and Isles of Scilly
GB-COV	Coventry
GB-CRY	Croydon
GB-CMA	Cumbria
GB-DAL	Darlington
GB-DEN	Denbighshire
GB-DER	Derby
GB-DBY	Derbyshire
GB-DRS	Derry City and Strabane
GB-DRS	Derry and Strabane
GB-DEV	Devon
GB-DNC	Doncaster
GB-DOR	Dorset
GB-DUD	Dudley
GB-DGY	Dumfries and Galloway
GB-DND	Dundee City
GB-DUR	Durham County
GB-DUR	County Durham
GB-EAL	Ealing
GB-EAY	East Ayrshire
GB-EDU	East Dunbartonshire
GB-ELN	East Lothian
GB-ERW	East Renfrewshire
GB-ERY	East Riding of Yorkshire
GB-ESX	East Sussex
GB-EDH	Edinburgh, City of
GB-ELS	Eilean Siar
GB-ENF	Enfield
GB-ESS	Essex
GB-FAL	Falkirk
GB-FMO	Fermanagh and Omagh
GB-FIF	Fife
GB-FLN	Flintshire
GB-GAT	Gateshead
GB-GLG	Glasgow City
GB-GLS	Gloucestershire
GB-GRE	Greenwich
GB-GWN	Gwynedd
GB-HCK	Hackney
GB-HAL	Halton
GB-HMF	Hammersmith and Fulham
GB-HAM	Hampshire
GB-HRY	Haringey
GB-HRW	Harrow
GB-HPL	Hartlepool
GB-HAV	Havering
GB-HEF	Herefordshire
GB-HEF	Herefordshire, County of
GB-HRT	Hertfordshire
GB-HLD	Highland
GB-HIL	Hillingdon
GB-HNS	Hounslow
GB-IVC	Inverclyde
GB-AGY	Isle of Anglesey
GB-IOW	Isle of Wight
GB-IOS	Isles of Scilly
GB-ISL	Islington
GB-KEC	Kensington and Chelsea
GB-KEN	Kent
GB-KHL	Kingston upon Hull
GB-KHL	Kingston upon Hull, City of
GB-KTT	Kingston upon Thames
GB-KIR	Kirklees
GB-KWL	Knowsley
GB-LBH	Lambeth
GB-LAN	Lancashire
GB-LDS	Leeds
GB-LCE	Leicester
GB-LEC	Leicestershire
GB-LEW	Lewisham
GB-LIN	Lincolnshire
GB-LBC	Lisburn and Castlereagh
GB-LIV	Liverpool
GB-LND	London, City of
GB-LND	City of London
GB-LUT	Luton
GB-MAN	Manchester
GB-MDW	Medway
GB-MTY	Merthyr Tydfil
GB-MRT	Merton
GB-MEA	Mid and East Antrim
GB-MUL	Mid Ulster
GB-MDB	Middlesbrough
GB-MLN	Midlothian
GB-MIK	Milton Keynes
GB-MON	Monmouthshire
GB-MRY	Moray
GB-NTL	Neath Port Talbot
GB-NET	Newcastle upon Tyne
GB-NWM	Newham
GB-NWP	Newport
GB-NMD	Newry, Mourne and Down
GB-NFK	Norfolk
GB-NAY	North Ayrshire
GB-NEL	North East Lincolnshire
GB-NLK	North Lanarkshire
GB-NLN	North Lincolnshire
GB-NSM	North Somerset
GB-NTY	North Tyneside
GB-NYK	North Yorkshire
GB-NTH	Northamptonshire
GB-NBL	Northumberland
GB-NGM	Nottingham
GB-NTT	Nottinghamshire
GB-OLD	Oldham
GB-ORK	Orkney Islands
GB-ORK	Orkney
GB-OXF	Oxfordshire
GB-PEM	Pembrokeshire
GB-PKN	Perth and Kinross
GB-PTE	Peterborough
GB-PLY	Plymouth
GB-POL	Poole
GB-POR	Portsmouth
GB-POW	Powys
GB-RDG	Reading
GB-RDB	Redbridge
GB-RCC	Redcar and Cleveland
GB-RFW	Renfrewshire
GB-RCT	Rhondda, Cynon, Taff
GB-RIC	Richmond upon Thames
GB-RCH	Rochdale
GB-ROT	Rotherham
GB-RUT	Rutland
GB-SLF	Salford
GB-SAW	Sandwell
GB-SCB	Scottish Borders, The
GB-SCB	Borders
GB-SFT	Sefton
GB-SHF	Sheffield
GB-ZET	Shetland Islands
GB-ZET	Shetland
GB-SHR	Shropshire
GB-SLG	Slough
GB-SOL	Solihull
GB-SOM	Somerset
GB-SAY	South Ayrshire
GB-SGC	South Gloucestershire
GB-SLK	South Lanarkshire
GB-STY	South Tyneside
GB-STH	Southampton
GB-SOS	Southend-on-Sea
GB-SWK	Southwark
GB-SHN	St. Helens
GB-STS	Staffordshire
GB-STG	Stirling
GB-SKP	Stockport
GB-STT	Stockton-on-Tees
GB-STE	Stoke-on-Trent
GB-SFK	Suffolk
GB-SND	Sunderland
GB-SRY	Surrey
GB-STN	Sutton
GB-SWA	Swansea
GB-SWD	Swindon
GB-TAM	Tameside
GB-TFW	Telford and Wrekin
GB-THR	Thurrock
GB-TOB	Torbay
GB-TOF	Torfaen
GB-TWH	Tower Hamlets
GB-TRF	Trafford
GB-VGL	Vale of Glamorgan
GB-WKF	Wakefield
GB-WLL	Walsall
GB-WFT	Waltham Forest
GB-WND	Wandsworth
GB-WRT	Warrington
GB-WAR	Warwickshire
GB-WBK	West Berkshire
GB-WDU	West Dunbartonshire
GB-WLN	West Lothian
GB-WSX	West Sussex
GB-WSM	Westminster
GB-WGN	Wigan
GB-WIL	Wiltshire
GB-WNM	Windsor and Maidenhead
GB-WRL	Wirral
GB-WOK	Wokingham
GB-WLV	Wolverhampton
GB-WOR	Worcestershire
GB-WRX	Wrexham
GB-YOR	York
Aneurin Bevan	Aneurin Bevan
Betsi Cadwaladr	Betsi Cadwaladr
Cwm Taf	Cwm Taf
Cardiff and Vale	Cardiff and Vale
Hywel Dda	Hywel Dda
Other	Outside Wales
Swansea Bay	Swansea Bay
Unknown	Unknown
Not Known	Not Known
Bournemouth, Christchurch and Poole	Bournemouth, Christchurch and Poole
Lothian	Lothian
Grampian	Grampian
Greater Glasgow and Clyde	Greater Glasgow and Clyde
Forth Valley	Forth Valley
Lanarkshire	Lanarkshire
Ayrshire and Arran	Ayrshire and Arran
Tayside	Tayside
Western Isles	Western Isles
""".strip().split('\n')])


class UKData(GithubRepo):
    SOURCE_URL = 'https://github.com/tomwhite/covid-19-uk-data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'gb_uk_unofficial'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'uk' / 'covid-19-uk-data' / 'data',
                            github_url='https://github.com/tomwhite/covid-19-uk-data')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases_uk())
        r.extend(self._get_indicators_uk())
        return r

    def _get_cases_uk(self):
        r = []

        # By area

        # Date,Country,AreaCode,Area,TotalCases
        # 2020-01-08,Wales,W11000028,Aneurin Bevan,0
        # 2020-01-08,Wales,W11000023,Betsi Cadwaladr,0
        # 2020-01-08,Wales,W11000029,Cardiff and Vale,0
        # 2020-01-08,Wales,W11000030,Cwm Taf,0
        # 2020-01-08,Wales,W11000025,Hywel Dda,0
        # 2020-01-08,Wales,,Outside Wales,0

        with open(self.get_path_in_dir('covid-19-cases-uk.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])
                if item['TotalCases'] == 'NaN':
                    continue

                if item['Country'] == 'England':
                    # England, Wales and Scotland all use different systems
                    # England is close to standard Admin1, but Wales
                    # and Scotland use their own hospital systems
                    area = place_map[item['Area']]
                else:
                    area = item['Area']

                r.append(DataPoint(
                    region_schema=SCHEMA_UK_AREA,
                    region_parent='GB', #item['Country'],
                    region_child=area,
                    datatype=DT_TOTAL,
                    value=int(item['TotalCases']),
                    date_updated=date,
                    source_url='https://github.com/tomwhite/covid-19-uk-data'
                ))

        return r

    def _get_indicators_uk(self):
        r = []

        # By country

        # Date,Country,Indicator,Value
        # 2020-01-08,Wales,ConfirmedCases,0
        # 2020-01-08,Wales,Tests,1
        # 2020-01-09,Wales,ConfirmedCases,0
        # 2020-01-09,Wales,Tests,1

        with open(self.get_path_in_dir('covid-19-indicators-uk.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])

                datatype_map = {
                    'ConfirmedCases': DT_TOTAL,
                    'Tests': DT_TESTS_TOTAL,
                    'Deaths': DT_STATUS_DEATHS
                }
                schema, parent, country = {
                    'UK': (SCHEMA_ADMIN_0, None, 'GB'),
                    'England': (SCHEMA_ADMIN_1, 'GB', 'GB-ENG'),
                    'Wales': (SCHEMA_ADMIN_1, 'GB', 'GB-WLS'),
                    'Scotland': (SCHEMA_ADMIN_1, 'GB', 'GB-SCT'),
                    'Northern Ireland': (SCHEMA_ADMIN_1, 'GB', 'GB-NIR'),
                }[item['Country']]

                r.append(DataPoint(
                    region_schema=schema,  # TODO: Should this be a separate schema?
                    region_parent=parent,
                    region_child=country,
                    datatype=datatype_map[item['Indicator'].strip()],
                    value=int(item['Value']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(UKData().get_datapoints())
