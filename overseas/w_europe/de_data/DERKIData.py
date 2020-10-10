# https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_1/

import json
import datetime
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir
from covid_19_au_grab.overseas.w_europe.de_data.DEData import state_to_name
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


name_to_state = {
    state.lower(): name for name, state in state_to_name.items()
}

KREIS_URL = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=cases%20desc&resultOffset=0&resultRecordCount=1000&resultType=standard&cacheHint=true'


class DERKIData(URLBase):
    SOURCE_URL = 'https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_1/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'de_rki_dash'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'de' / 'data',
            urls_dict={
                'kreis.json': URL(KREIS_URL, static_file=False),
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('de_kreis', 'de-bb', 'barnim'): ('de_kreis', 'de-bb', 'barnim'),
                ('de_kreis', 'de-bb', 'brandenburg an der havel städte'): ('de_kreis', 'de-bb', 'brandenburg an der havel städte'),
                ('de_kreis', 'de-bb', 'cottbus städte'): ('de_kreis', 'de-bb', 'cottbus städte'),
                ('de_kreis', 'de-bb', 'dahme-spreewald'): ('de_kreis', 'de-bb', 'dahme-spreewald'),
                ('de_kreis', 'de-bb', 'elbe-elster'): ('de_kreis', 'de-bb', 'elbe-elster'),
                ('de_kreis', 'de-bb', 'frankfurt (oder) städte'): ('de_kreis', 'de-bb', 'Frankfurt am Oder Städte'),
                ('de_kreis', 'de-bb', 'havelland'): ('de_kreis', 'de-bb', 'havelland'),
                ('de_kreis', 'de-bb', 'märkisch-oderland'): ('de_kreis', 'de-bb', 'märkisch-oderland'),
                ('de_kreis', 'de-bb', 'oberhavel'): ('de_kreis', 'de-bb', 'oberhavel'),
                ('de_kreis', 'de-bb', 'oberspreewald-lausitz'): ('de_kreis', 'de-bb', 'oberspreewald-lausitz'),
                ('de_kreis', 'de-bb', 'oder-spree'): ('de_kreis', 'de-bb', 'oder-spree'),
                ('de_kreis', 'de-bb', 'ostprignitz-ruppin'): ('de_kreis', 'de-bb', 'ostprignitz-ruppin'),
                ('de_kreis', 'de-bb', 'potsdam städte'): ('de_kreis', 'de-bb', 'potsdam städte'),
                ('de_kreis', 'de-bb', 'potsdam-mittelmark'): ('de_kreis', 'de-bb', 'potsdam-mittelmark'),
                ('de_kreis', 'de-bb', 'prignitz'): ('de_kreis', 'de-bb', 'prignitz'),
                ('de_kreis', 'de-bb', 'spree-neiße'): ('de_kreis', 'de-bb', 'spree-neiße'),
                ('de_kreis', 'de-bb', 'teltow-fläming'): ('de_kreis', 'de-bb', 'teltow-fläming'),
                ('de_kreis', 'de-bb', 'uckermark'): ('de_kreis', 'de-bb', 'uckermark'),
                ('de_kreis', 'de-be', 'berlin charlottenburg-wilmersdorf'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin friedrichshain-kreuzberg'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin lichtenberg'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin marzahn-hellersdorf'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin mitte'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin neukölln'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin pankow'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin reinickendorf'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin spandau'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin steglitz-zehlendorf'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin tempelhof-schöneberg'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-be', 'berlin treptow-köpenick'): ('MERGE', 'de_kreis', 'de-be', 'berlin'),
                ('de_kreis', 'de-bw', 'alb-donau-kreis'): ('de_kreis', 'de-bw', 'Alb-Donau'),
                ('de_kreis', 'de-bw', 'baden-baden städte'): ('de_kreis', 'de-bw', 'baden-baden städte'),
                ('de_kreis', 'de-bw', 'biberach'): ('de_kreis', 'de-bw', 'biberach'),
                ('de_kreis', 'de-bw', 'bodenseekreis'): ('de_kreis', 'de-bw', 'Bodensee'),
                ('de_kreis', 'de-bw', 'breisgau-hochschwarzwald'): ('de_kreis', 'de-bw', 'breisgau-hochschwarzwald'),
                ('de_kreis', 'de-bw', 'böblingen'): ('de_kreis', 'de-bw', 'böblingen'),
                ('de_kreis', 'de-bw', 'calw'): ('de_kreis', 'de-bw', 'calw'),
                ('de_kreis', 'de-bw', 'emmendingen'): ('de_kreis', 'de-bw', 'emmendingen'),
                ('de_kreis', 'de-bw', 'enzkreis'): ('de_kreis', 'de-bw', 'Enz'),
                ('de_kreis', 'de-bw', 'esslingen'): ('de_kreis', 'de-bw', 'esslingen'),
                ('de_kreis', 'de-bw', 'freiburg im breisgau städte'): ('de_kreis', 'de-bw', 'Breisgau-Hochschwarzwald'),
                ('de_kreis', 'de-bw', 'freudenstadt'): ('de_kreis', 'de-bw', 'freudenstadt'),
                ('de_kreis', 'de-bw', 'göppingen'): ('de_kreis', 'de-bw', 'göppingen'),
                ('de_kreis', 'de-bw', 'heidelberg städte'): ('de_kreis', 'de-bw', 'heidelberg städte'),
                ('de_kreis', 'de-bw', 'heidenheim'): ('de_kreis', 'de-bw', 'heidenheim'),
                ('de_kreis', 'de-bw', 'heilbronn'): ('de_kreis', 'de-bw', 'heilbronn'),
                ('de_kreis', 'de-bw', 'heilbronn städte'): ('de_kreis', 'de-bw', 'Heilbronn city Städte'),
                ('de_kreis', 'de-bw', 'hohenlohekreis'): ('de_kreis', 'de-bw', 'Hohenlohe'),
                ('de_kreis', 'de-bw', 'karlsruhe'): ('de_kreis', 'de-bw', 'karlsruhe'),
                ('de_kreis', 'de-bw', 'karlsruhe städte'): ('de_kreis', 'de-bw', 'karlsruhe städte'),
                ('de_kreis', 'de-bw', 'konstanz'): ('de_kreis', 'de-bw', 'konstanz'),
                ('de_kreis', 'de-bw', 'ludwigsburg'): ('de_kreis', 'de-bw', 'ludwigsburg'),
                ('de_kreis', 'de-bw', 'lörrach'): ('de_kreis', 'de-bw', 'lörrach'),
                ('de_kreis', 'de-bw', 'main-tauber-kreis'): ('de_kreis', 'de-bw', 'Main-Tauber'),
                ('de_kreis', 'de-bw', 'mannheim städte'): ('de_kreis', 'de-bw', 'mannheim städte'),
                ('de_kreis', 'de-bw', 'neckar-odenwald-kreis'): ('de_kreis', 'de-bw', 'neckar-odenwald-kreis'),
                ('de_kreis', 'de-bw', 'ortenaukreis'): ('de_kreis', 'de-bw', 'ortenaukreis'),
                ('de_kreis', 'de-bw', 'ostalbkreis'): ('de_kreis', 'de-bw', 'ostalbkreis'),
                ('de_kreis', 'de-bw', 'pforzheim städte'): ('de_kreis', 'de-bw', 'pforzheim städte'),
                ('de_kreis', 'de-bw', 'rastatt'): ('de_kreis', 'de-bw', 'rastatt'),
                ('de_kreis', 'de-bw', 'ravensburg'): ('de_kreis', 'de-bw', 'ravensburg'),
                ('de_kreis', 'de-bw', 'rems-murr-kreis'): ('de_kreis', 'de-bw', 'rems-murr-kreis'),
                ('de_kreis', 'de-bw', 'reutlingen'): ('de_kreis', 'de-bw', 'reutlingen'),
                ('de_kreis', 'de-bw', 'rhein-neckar-kreis'): ('de_kreis', 'de-bw', 'rhein-neckar-kreis'),
                ('de_kreis', 'de-bw', 'rottweil'): ('de_kreis', 'de-bw', 'rottweil'),
                ('de_kreis', 'de-bw', 'schwarzwald-baar-kreis'): ('de_kreis', 'de-bw', 'schwarzwald-baar-kreis'),
                ('de_kreis', 'de-bw', 'schwäbisch hall'): ('de_kreis', 'de-bw', 'schwäbisch hall'),
                ('de_kreis', 'de-bw', 'sigmaringen'): ('de_kreis', 'de-bw', 'sigmaringen'),
                ('de_kreis', 'de-bw', 'stuttgart städte'): ('de_kreis', 'de-bw', 'stuttgart städte'),
                ('de_kreis', 'de-bw', 'tuttlingen'): ('de_kreis', 'de-bw', 'tuttlingen'),
                ('de_kreis', 'de-bw', 'tübingen'): ('de_kreis', 'de-bw', 'tübingen'),
                ('de_kreis', 'de-bw', 'ulm städte'): ('de_kreis', 'de-bw', 'ulm städte'),
                ('de_kreis', 'de-bw', 'waldshut'): ('de_kreis', 'de-bw', 'waldshut'),
                ('de_kreis', 'de-bw', 'zollernalbkreis'): ('de_kreis', 'de-bw', 'zollernalbkreis'),
                ('de_kreis', 'de-by', 'aichach-friedberg'): ('de_kreis', 'de-by', 'aichach-friedberg'),
                ('de_kreis', 'de-by', 'altötting'): ('de_kreis', 'de-by', 'altötting'),
                ('de_kreis', 'de-by', 'amberg städte'): ('de_kreis', 'de-by', 'amberg städte'),
                ('de_kreis', 'de-by', 'amberg-sulzbach'): ('de_kreis', 'de-by', 'amberg-sulzbach'),
                ('de_kreis', 'de-by', 'ansbach'): ('de_kreis', 'de-by', 'ansbach'),
                ('de_kreis', 'de-by', 'ansbach städte'): ('de_kreis', 'de-by', 'ansbach städte'),
                ('de_kreis', 'de-by', 'aschaffenburg'): ('de_kreis', 'de-by', 'aschaffenburg'),
                ('de_kreis', 'de-by', 'aschaffenburg städte'): ('de_kreis', 'de-by', 'aschaffenburg städte'),
                ('de_kreis', 'de-by', 'augsburg'): ('de_kreis', 'de-by', 'augsburg'),
                ('de_kreis', 'de-by', 'augsburg städte'): ('de_kreis', 'de-by', 'augsburg städte'),
                ('de_kreis', 'de-by', 'bad kissingen'): ('de_kreis', 'de-by', 'bad kissingen'),
                ('de_kreis', 'de-by', 'bad tölz-wolfratshausen'): ('de_kreis', 'de-by', 'bad tölz-wolfratshausen'),
                ('de_kreis', 'de-by', 'bamberg'): ('de_kreis', 'de-by', 'bamberg'),
                ('de_kreis', 'de-by', 'bamberg städte'): ('de_kreis', 'de-by', 'bamberg städte'),
                ('de_kreis', 'de-by', 'bayreuth'): ('de_kreis', 'de-by', 'bayreuth'),
                ('de_kreis', 'de-by', 'bayreuth städte'): ('de_kreis', 'de-by', 'bayreuth städte'),
                ('de_kreis', 'de-by', 'berchtesgadener land'): ('de_kreis', 'de-by', 'berchtesgadener land'),
                ('de_kreis', 'de-by', 'cham'): ('de_kreis', 'de-by', 'cham'),
                ('de_kreis', 'de-by', 'coburg'): ('de_kreis', 'de-by', 'coburg'),
                ('de_kreis', 'de-by', 'coburg städte'): ('de_kreis', 'de-by', 'coburg städte'),
                ('de_kreis', 'de-by', 'dachau'): ('de_kreis', 'de-by', 'dachau'),
                ('de_kreis', 'de-by', 'deggendorf'): ('de_kreis', 'de-by', 'deggendorf'),
                ('de_kreis', 'de-by', 'dillingen a.d. donau'): ('de_kreis', 'de-by', 'dillingen'),
                ('de_kreis', 'de-by', 'dingolfing-landau'): ('de_kreis', 'de-by', 'dingolfing-landau'),
                ('de_kreis', 'de-by', 'donau-ries'): ('de_kreis', 'de-by', 'donau-ries'),
                ('de_kreis', 'de-by', 'ebersberg'): ('de_kreis', 'de-by', 'ebersberg'),
                ('de_kreis', 'de-by', 'eichstätt'): ('de_kreis', 'de-by', 'eichstätt'),
                ('de_kreis', 'de-by', 'erding'): ('de_kreis', 'de-by', 'erding'),
                ('de_kreis', 'de-by', 'erlangen städte'): ('de_kreis', 'de-by', 'erlangen städte'),
                ('de_kreis', 'de-by', 'erlangen-höchstadt'): ('de_kreis', 'de-by', 'erlangen-höchstadt'),
                ('de_kreis', 'de-by', 'forchheim'): ('de_kreis', 'de-by', 'forchheim'),
                ('de_kreis', 'de-by', 'freising'): ('de_kreis', 'de-by', 'freising'),
                ('de_kreis', 'de-by', 'freyung-grafenau'): ('de_kreis', 'de-by', 'freyung-grafenau'),
                ('de_kreis', 'de-by', 'fürstenfeldbruck'): ('de_kreis', 'de-by', 'fürstenfeldbruck'),
                ('de_kreis', 'de-by', 'fürth'): ('de_kreis', 'de-by', 'fürth'),
                ('de_kreis', 'de-by', 'fürth städte'): ('de_kreis', 'de-by', 'fürth städte'),
                ('de_kreis', 'de-by', 'garmisch-partenkirchen'): ('de_kreis', 'de-by', 'garmisch-partenkirchen'),
                ('de_kreis', 'de-by', 'günzburg'): ('de_kreis', 'de-by', 'günzburg'),
                ('de_kreis', 'de-by', 'haßberge'): ('de_kreis', 'de-by', 'haßberge'),
                ('de_kreis', 'de-by', 'hof'): ('de_kreis', 'de-by', 'hof'),
                ('de_kreis', 'de-by', 'hof städte'): ('de_kreis', 'de-by', 'hof städte'),
                ('de_kreis', 'de-by', 'ingolstadt städte'): ('de_kreis', 'de-by', 'ingolstadt städte'),
                ('de_kreis', 'de-by', 'kaufbeuren städte'): ('de_kreis', 'de-by', 'kaufbeuren städte'),
                ('de_kreis', 'de-by', 'kelheim'): ('de_kreis', 'de-by', 'kelheim'),
                ('de_kreis', 'de-by', 'kempten (allgäu) städte'): ('de_kreis', 'de-by', 'Kempten Städte'),
                ('de_kreis', 'de-by', 'kitzingen'): ('de_kreis', 'de-by', 'kitzingen'),
                ('de_kreis', 'de-by', 'kronach'): ('de_kreis', 'de-by', 'kronach'),
                ('de_kreis', 'de-by', 'kulmbach'): ('de_kreis', 'de-by', 'kulmbach'),
                ('de_kreis', 'de-by', 'landsberg am lech'): ('de_kreis', 'de-by', 'Landsberg'),
                ('de_kreis', 'de-by', 'landshut'): ('de_kreis', 'de-by', 'landshut'),
                ('de_kreis', 'de-by', 'landshut städte'): ('de_kreis', 'de-by', 'landshut städte'),
                ('de_kreis', 'de-by', 'lichtenfels'): ('de_kreis', 'de-by', 'lichtenfels'),
                ('de_kreis', 'de-by', 'lindau (bodensee)'): ('de_kreis', 'de-by', 'Lindau'),
                ('de_kreis', 'de-by', 'main-spessart'): ('de_kreis', 'de-by', 'main-spessart'),
                ('de_kreis', 'de-by', 'memmingen städte'): ('de_kreis', 'de-by', 'memmingen städte'),
                ('de_kreis', 'de-by', 'miesbach'): ('de_kreis', 'de-by', 'miesbach'),
                ('de_kreis', 'de-by', 'miltenberg'): ('de_kreis', 'de-by', 'miltenberg'),
                ('de_kreis', 'de-by', 'mühldorf a. inn'): ('de_kreis', 'de-by', 'mühldorf'),
                ('de_kreis', 'de-by', 'münchen'): ('de_kreis', 'de-by', 'münchen'),
                ('de_kreis', 'de-by', 'münchen städte'): ('de_kreis', 'de-by', 'münchen'),
                ('de_kreis', 'de-by', 'neu-ulm'): ('de_kreis', 'de-by', 'neu-ulm'),
                ('de_kreis', 'de-by', 'neuburg-schrobenhausen'): ('de_kreis', 'de-by', 'neuburg-schrobenhausen'),
                ('de_kreis', 'de-by', 'neumarkt i.d. opf.'): ('de_kreis', 'de-by', 'Neumarkt'),
                ('de_kreis', 'de-by', 'neustadt a.d. aisch-bad windsheim'): ('de_kreis', 'de-by', 'Neustadt-Bad Windsheim'),
                ('de_kreis', 'de-by', 'neustadt a.d. waldnaab'): ('de_kreis', 'de-by', 'Neustadt'),
                ('de_kreis', 'de-by', 'nürnberg städte'): ('de_kreis', 'de-by', 'Nuremberg Städte'),
                ('de_kreis', 'de-by', 'nürnberger land'): ('de_kreis', 'de-by', 'nürnberger land'),
                ('de_kreis', 'de-by', 'oberallgäu'): ('de_kreis', 'de-by', 'oberallgäu'),
                ('de_kreis', 'de-by', 'ostallgäu'): ('de_kreis', 'de-by', 'ostallgäu'),
                ('de_kreis', 'de-by', 'passau'): ('de_kreis', 'de-by', 'passau'),
                ('de_kreis', 'de-by', 'passau städte'): ('de_kreis', 'de-by', 'passau städte'),
                ('de_kreis', 'de-by', 'pfaffenhofen a.d. ilm'): ('de_kreis', 'de-by', 'Pfaffenhofen'),
                ('de_kreis', 'de-by', 'regen'): ('de_kreis', 'de-by', 'regen'),
                ('de_kreis', 'de-by', 'regensburg'): ('de_kreis', 'de-by', 'regensburg'),
                ('de_kreis', 'de-by', 'regensburg städte'): ('de_kreis', 'de-by', 'regensburg städte'),
                ('de_kreis', 'de-by', 'rhön-grabfeld'): ('de_kreis', 'de-by', 'rhön-grabfeld'),
                ('de_kreis', 'de-by', 'rosenheim'): ('de_kreis', 'de-by', 'rosenheim'),
                ('de_kreis', 'de-by', 'rosenheim städte'): ('de_kreis', 'de-by', 'rosenheim städte'),
                ('de_kreis', 'de-by', 'roth'): ('de_kreis', 'de-by', 'roth'),
                ('de_kreis', 'de-by', 'rottal-inn'): ('de_kreis', 'de-by', 'rottal-inn'),
                ('de_kreis', 'de-by', 'schwabach städte'): ('de_kreis', 'de-by', 'schwabach städte'),
                ('de_kreis', 'de-by', 'schwandorf'): ('de_kreis', 'de-by', 'schwandorf'),
                ('de_kreis', 'de-by', 'schweinfurt'): ('de_kreis', 'de-by', 'schweinfurt'),
                ('de_kreis', 'de-by', 'schweinfurt städte'): ('de_kreis', 'de-by', 'schweinfurt städte'),
                ('de_kreis', 'de-by', 'starnberg'): ('de_kreis', 'de-by', 'starnberg'),
                ('de_kreis', 'de-by', 'straubing städte'): ('de_kreis', 'de-by', 'straubing städte'),
                ('de_kreis', 'de-by', 'straubing-bogen'): ('de_kreis', 'de-by', 'straubing-bogen'),
                ('de_kreis', 'de-by', 'tirschenreuth'): ('de_kreis', 'de-by', 'tirschenreuth'),
                ('de_kreis', 'de-by', 'traunstein'): ('de_kreis', 'de-by', 'traunstein'),
                ('de_kreis', 'de-by', 'unterallgäu'): ('de_kreis', 'de-by', 'unterallgäu'),
                ('de_kreis', 'de-by', 'weiden i.d. opf. städte'): ('de_kreis', 'de-by', 'Weiden Städte'),
                ('de_kreis', 'de-by', 'weilheim-schongau'): ('de_kreis', 'de-by', 'weilheim-schongau'),
                ('de_kreis', 'de-by', 'weißenburg-gunzenhausen'): ('de_kreis', 'de-by', 'weißenburg-gunzenhausen'),
                ('de_kreis', 'de-by', 'wunsiedel i. fichtelgebirge'): ('de_kreis', 'de-by', 'Wunsiedel'),
                ('de_kreis', 'de-by', 'würzburg'): ('de_kreis', 'de-by', 'würzburg'),
                ('de_kreis', 'de-by', 'würzburg städte'): ('de_kreis', 'de-by', 'würzburg städte'),
                ('de_kreis', 'de-hb', 'bremen städte'): ('de_kreis', 'de-hb', 'bremen städte'),
                ('de_kreis', 'de-hb', 'bremerhaven städte'): None,
                ('de_kreis', 'de-he', 'bergstraße'): ('de_kreis', 'de-he', 'bergstraße'),
                ('de_kreis', 'de-he', 'darmstadt städte'): ('de_kreis', 'de-he', 'darmstadt städte'),
                ('de_kreis', 'de-he', 'darmstadt-dieburg'): ('de_kreis', 'de-he', 'darmstadt-dieburg'),
                ('de_kreis', 'de-he', 'frankfurt am main städte'): ('de_kreis', 'de-he', 'frankfurt am main städte'),
                ('de_kreis', 'de-he', 'fulda'): ('de_kreis', 'de-he', 'fulda'),
                ('de_kreis', 'de-he', 'gießen'): ('de_kreis', 'de-he', 'gießen'),
                ('de_kreis', 'de-he', 'groß-gerau'): ('de_kreis', 'de-he', 'groß-gerau'),
                ('de_kreis', 'de-he', 'hersfeld-rotenburg'): ('de_kreis', 'de-he', 'hersfeld-rotenburg'),
                ('de_kreis', 'de-he', 'hochtaunuskreis'): ('de_kreis', 'de-he', 'hochtaunuskreis'),
                ('de_kreis', 'de-he', 'kassel'): ('de_kreis', 'de-he', 'kassel'),
                ('de_kreis', 'de-he', 'kassel städte'): ('de_kreis', 'de-he', 'kassel städte'),
                ('de_kreis', 'de-he', 'lahn-dill-kreis'): ('de_kreis', 'de-he', 'lahn-dill-kreis'),
                ('de_kreis', 'de-he', 'limburg-weilburg'): ('de_kreis', 'de-he', 'limburg-weilburg'),
                ('de_kreis', 'de-he', 'main-kinzig-kreis'): ('de_kreis', 'de-he', 'main-kinzig-kreis'),
                ('de_kreis', 'de-he', 'main-taunus-kreis'): ('de_kreis', 'de-he', 'Main-Taunus-Kreis Städte'),
                ('de_kreis', 'de-he', 'marburg-biedenkopf'): ('de_kreis', 'de-he', 'marburg-biedenkopf'),
                ('de_kreis', 'de-he', 'odenwaldkreis'): ('de_kreis', 'de-he', 'odenwaldkreis'),
                ('de_kreis', 'de-he', 'offenbach'): ('de_kreis', 'de-he', 'offenbach'),
                ('de_kreis', 'de-he', 'offenbach am main städte'): ('de_kreis', 'de-he', 'offenbach am main städte'),
                ('de_kreis', 'de-he', 'rheingau-taunus-kreis'): ('de_kreis', 'de-he', 'rheingau-taunus-kreis'),
                ('de_kreis', 'de-he', 'schwalm-eder-kreis'): ('de_kreis', 'de-he', 'schwalm-eder-kreis'),
                ('de_kreis', 'de-he', 'vogelsbergkreis'): ('de_kreis', 'de-he', 'vogelsbergkreis'),
                ('de_kreis', 'de-he', 'waldeck-frankenberg'): ('de_kreis', 'de-he', 'waldeck-frankenberg'),
                ('de_kreis', 'de-he', 'werra-meißner-kreis'): ('de_kreis', 'de-he', 'werra-meißner-kreis'),
                ('de_kreis', 'de-he', 'wetteraukreis'): ('de_kreis', 'de-he', 'wetteraukreis'),
                ('de_kreis', 'de-he', 'wiesbaden städte'): ('de_kreis', 'de-he', 'wiesbaden städte'),
                ('de_kreis', 'de-hh', 'hamburg städte'): ('de_kreis', 'de-hh', 'hamburg städte'),
                ('de_kreis', 'de-mv', 'ludwigslust-parchim'): ('de_kreis', 'de-mv', 'ludwigslust'),
                ('de_kreis', 'de-mv', 'mecklenburgische seenplatte'): None,
                ('de_kreis', 'de-mv', 'nordwestmecklenburg'): ('de_kreis', 'de-mv', 'nordwestmecklenburg'),
                ('de_kreis', 'de-mv', 'rostock'): ('MERGE', 'de_kreis', 'de-mv', 'rostock städte'),
                ('de_kreis', 'de-mv', 'rostock städte'): ('MERGE', 'de_kreis', 'de-mv', 'rostock städte'),
                ('de_kreis', 'de-mv', 'schwerin städte'): ('de_kreis', 'de-mv', 'schwerin städte'),
                ('de_kreis', 'de-mv', 'vorpommern-greifswald'): ('de_kreis', 'de-mv', 'Greifswald Städte'),
                ('de_kreis', 'de-mv', 'vorpommern-rügen'): ('de_kreis', 'de-mv', 'Rügen'),
                ('de_kreis', 'de-ni', 'ammerland'): ('de_kreis', 'de-ni', 'ammerland'),
                ('de_kreis', 'de-ni', 'aurich'): ('de_kreis', 'de-ni', 'aurich'),
                ('de_kreis', 'de-ni', 'braunschweig städte'): ('de_kreis', 'de-ni', 'braunschweig städte'),
                ('de_kreis', 'de-ni', 'celle'): ('de_kreis', 'de-ni', 'celle'),
                ('de_kreis', 'de-ni', 'cloppenburg'): ('de_kreis', 'de-ni', 'cloppenburg'),
                ('de_kreis', 'de-ni', 'cuxhaven'): ('de_kreis', 'de-ni', 'cuxhaven'),
                ('de_kreis', 'de-ni', 'delmenhorst städte'): None,
                ('de_kreis', 'de-ni', 'diepholz'): ('de_kreis', 'de-ni', 'diepholz'),
                ('de_kreis', 'de-ni', 'emden städte'): ('de_kreis', 'de-ni', 'emden städte'),
                ('de_kreis', 'de-ni', 'emsland'): ('de_kreis', 'de-ni', 'emsland'),
                ('de_kreis', 'de-ni', 'friesland'): ('de_kreis', 'de-ni', 'friesland'),
                ('de_kreis', 'de-ni', 'gifhorn'): ('de_kreis', 'de-ni', 'gifhorn'),
                ('de_kreis', 'de-ni', 'goslar'): ('de_kreis', 'de-ni', 'goslar'),
                ('de_kreis', 'de-ni', 'grafschaft bentheim'): ('de_kreis', 'de-ni', 'grafschaft bentheim'),
                ('de_kreis', 'de-ni', 'göttingen'): ('de_kreis', 'de-ni', 'göttingen'),
                ('de_kreis', 'de-ni', 'hameln-pyrmont'): ('de_kreis', 'de-ni', 'Hamelin-Pyrmont'),
                ('de_kreis', 'de-ni', 'harburg'): ('de_kreis', 'de-ni', 'harburg'),
                ('de_kreis', 'de-ni', 'heidekreis'): None,
                ('de_kreis', 'de-ni', 'helmstedt'): ('de_kreis', 'de-ni', 'helmstedt'),
                ('de_kreis', 'de-ni', 'hildesheim'): ('de_kreis', 'de-ni', 'hildesheim'),
                ('de_kreis', 'de-ni', 'holzminden'): ('de_kreis', 'de-ni', 'holzminden'),
                ('de_kreis', 'de-ni', 'leer'): ('de_kreis', 'de-ni', 'leer'),
                ('de_kreis', 'de-ni', 'lüchow-dannenberg'): ('de_kreis', 'de-ni', 'lüchow-dannenberg'),
                ('de_kreis', 'de-ni', 'lüneburg'): ('de_kreis', 'de-ni', 'lüneburg'),
                ('de_kreis', 'de-ni', 'nienburg (weser)'): ('de_kreis', 'de-ni', 'Nienburg'),
                ('de_kreis', 'de-ni', 'northeim'): ('de_kreis', 'de-ni', 'northeim'),
                ('de_kreis', 'de-ni', 'oldenburg'): ('de_kreis', 'de-ni', 'oldenburg'),
                ('de_kreis', 'de-ni', 'oldenburg (oldb) städte'): ('de_kreis', 'de-ni', 'Oldenburg Städte'),
                ('de_kreis', 'de-ni', 'osnabrück'): ('de_kreis', 'de-ni', 'osnabrück'),
                ('de_kreis', 'de-ni', 'osnabrück städte'): ('de_kreis', 'de-ni', 'osnabrück städte'),
                ('de_kreis', 'de-ni', 'osterholz'): ('de_kreis', 'de-ni', 'osterholz'),
                ('de_kreis', 'de-ni', 'peine'): ('de_kreis', 'de-ni', 'peine'),
                ('de_kreis', 'de-ni', 'region hannover'): ('de_kreis', 'de-ni', 'Hanover'),
                ('de_kreis', 'de-ni', 'rotenburg (wümme)'): ('de_kreis', 'de-ni', 'rotenburg'),
                ('de_kreis', 'de-ni', 'salzgitter städte'): ('de_kreis', 'de-ni', 'salzgitter städte'),
                ('de_kreis', 'de-ni', 'schaumburg'): ('de_kreis', 'de-ni', 'schaumburg'),
                ('de_kreis', 'de-ni', 'stade'): ('de_kreis', 'de-ni', 'stade'),
                ('de_kreis', 'de-ni', 'uelzen'): ('de_kreis', 'de-ni', 'uelzen'),
                ('de_kreis', 'de-ni', 'vechta'): ('de_kreis', 'de-ni', 'vechta'),
                ('de_kreis', 'de-ni', 'verden'): ('de_kreis', 'de-ni', 'verden'),
                ('de_kreis', 'de-ni', 'wesermarsch'): ('de_kreis', 'de-ni', 'wesermarsch'),
                ('de_kreis', 'de-ni', 'wilhelmshaven städte'): ('de_kreis', 'de-ni', 'wilhelmshaven städte'),
                ('de_kreis', 'de-ni', 'wittmund'): ('de_kreis', 'de-ni', 'wittmund'),
                ('de_kreis', 'de-ni', 'wolfenbüttel'): ('de_kreis', 'de-ni', 'wolfenbüttel'),
                ('de_kreis', 'de-ni', 'wolfsburg städte'): ('de_kreis', 'de-ni', 'wolfsburg städte'),
                ('de_kreis', 'de-nw', 'bielefeld städte'): ('de_kreis', 'de-nw', 'bielefeld städte'),
                ('de_kreis', 'de-nw', 'bochum städte'): ('de_kreis', 'de-nw', 'bochum städte'),
                ('de_kreis', 'de-nw', 'bonn städte'): ('de_kreis', 'de-nw', 'bonn städte'),
                ('de_kreis', 'de-nw', 'borken'): ('de_kreis', 'de-nw', 'borken'),
                ('de_kreis', 'de-nw', 'bottrop städte'): ('de_kreis', 'de-nw', 'bottrop städte'),
                ('de_kreis', 'de-nw', 'coesfeld'): ('de_kreis', 'de-nw', 'coesfeld'),
                ('de_kreis', 'de-nw', 'dortmund städte'): ('de_kreis', 'de-nw', 'dortmund städte'),
                ('de_kreis', 'de-nw', 'duisburg städte'): ('de_kreis', 'de-nw', 'duisburg städte'),
                ('de_kreis', 'de-nw', 'düren'): ('de_kreis', 'de-nw', 'düren'),
                ('de_kreis', 'de-nw', 'düsseldorf städte'): ('de_kreis', 'de-nw', 'düsseldorf städte'),
                ('de_kreis', 'de-nw', 'ennepe-ruhr-kreis'): ('de_kreis', 'de-nw', 'Ennepe-Ruhr'),
                ('de_kreis', 'de-nw', 'essen städte'): ('de_kreis', 'de-nw', 'essen städte'),
                ('de_kreis', 'de-nw', 'euskirchen'): ('de_kreis', 'de-nw', 'euskirchen'),
                ('de_kreis', 'de-nw', 'gelsenkirchen städte'): ('de_kreis', 'de-nw', 'gelsenkirchen städte'),
                ('de_kreis', 'de-nw', 'gütersloh'): ('de_kreis', 'de-nw', 'gütersloh'),
                ('de_kreis', 'de-nw', 'hagen städte'): ('de_kreis', 'de-nw', 'hagen städte'),
                ('de_kreis', 'de-nw', 'hamm städte'): ('de_kreis', 'de-nw', 'hamm städte'),
                ('de_kreis', 'de-nw', 'heinsberg'): ('de_kreis', 'de-nw', 'heinsberg'),
                ('de_kreis', 'de-nw', 'herford'): ('de_kreis', 'de-nw', 'herford'),
                ('de_kreis', 'de-nw', 'herne städte'): ('de_kreis', 'de-nw', 'herne städte'),
                ('de_kreis', 'de-nw', 'hochsauerlandkreis'): ('de_kreis', 'de-nw', 'hochsauerlandkreis'),
                ('de_kreis', 'de-nw', 'höxter'): ('de_kreis', 'de-nw', 'höxter'),
                ('de_kreis', 'de-nw', 'kleve'): ('de_kreis', 'de-nw', 'Cleves'),
                ('de_kreis', 'de-nw', 'krefeld städte'): ('de_kreis', 'de-nw', 'krefeld städte'),
                ('de_kreis', 'de-nw', 'köln städte'): ('de_kreis', 'de-nw', 'Cologne Städte'),
                ('de_kreis', 'de-nw', 'leverkusen städte'): ('de_kreis', 'de-nw', 'leverkusen städte'),
                ('de_kreis', 'de-nw', 'lippe'): ('de_kreis', 'de-nw', 'lippe'),
                ('de_kreis', 'de-nw', 'mettmann'): ('de_kreis', 'de-nw', 'mettmann'),
                ('de_kreis', 'de-nw', 'minden-lübbecke'): ('de_kreis', 'de-nw', 'minden-lübbecke'),
                ('de_kreis', 'de-nw', 'märkischer kreis'): ('de_kreis', 'de-nw', 'märkischer kreis'),
                ('de_kreis', 'de-nw', 'mönchengladbach städte'): ('de_kreis', 'de-nw', 'mönchengladbach städte'),
                ('de_kreis', 'de-nw', 'mülheim an der ruhr städte'): ('de_kreis', 'de-nw', 'Mülheim Städte'),
                ('de_kreis', 'de-nw', 'münster städte'): ('de_kreis', 'de-nw', 'münster städte'),
                ('de_kreis', 'de-nw', 'oberbergischer kreis'): ('de_kreis', 'de-nw', 'oberbergischer kreis'),
                ('de_kreis', 'de-nw', 'oberhausen städte'): ('de_kreis', 'de-nw', 'oberhausen städte'),
                ('de_kreis', 'de-nw', 'olpe'): ('de_kreis', 'de-nw', 'olpe'),
                ('de_kreis', 'de-nw', 'paderborn'): ('de_kreis', 'de-nw', 'paderborn'),
                ('de_kreis', 'de-nw', 'recklinghausen'): ('de_kreis', 'de-nw', 'recklinghausen'),
                ('de_kreis', 'de-nw', 'remscheid städte'): ('de_kreis', 'de-nw', 'remscheid städte'),
                ('de_kreis', 'de-nw', 'rhein-erft-kreis'): ('de_kreis', 'de-nw', 'rhein-erft-kreis'),
                ('de_kreis', 'de-nw', 'rhein-kreis neuss'): ('de_kreis', 'de-nw', 'rhein-kreis neuss'),
                ('de_kreis', 'de-nw', 'rhein-sieg'): ('de_kreis', 'de-nw', 'rhein-sieg'),
                ('de_kreis', 'de-nw', 'rhein-sieg-kreis'): ('de_kreis', 'de-nw', 'rhein-sieg'),
                ('de_kreis', 'de-nw', 'rheinisch-bergischer kreis'): ('de_kreis', 'de-nw', 'rheinisch-bergischer kreis'),
                ('de_kreis', 'de-nw', 'siegen-wittgenstein'): ('de_kreis', 'de-nw', 'siegen-wittgenstein'),
                ('de_kreis', 'de-nw', 'soest'): ('de_kreis', 'de-nw', 'soest'),
                ('de_kreis', 'de-nw', 'solingen städte'): ('de_kreis', 'de-nw', 'solingen städte'),
                ('de_kreis', 'de-nw', 'steinfurt'): ('de_kreis', 'de-nw', 'steinfurt'),
                ('de_kreis', 'de-nw', 'städteregion aachen'): ('de_kreis', 'de-nw', 'Aachen Städte'),
                ('de_kreis', 'de-nw', 'unna'): ('de_kreis', 'de-nw', 'unna'),
                ('de_kreis', 'de-nw', 'viersen'): ('de_kreis', 'de-nw', 'viersen'),
                ('de_kreis', 'de-nw', 'warendorf'): ('de_kreis', 'de-nw', 'warendorf'),
                ('de_kreis', 'de-nw', 'wesel'): ('de_kreis', 'de-nw', 'wesel'),
                ('de_kreis', 'de-nw', 'wuppertal städte'): ('de_kreis', 'de-nw', 'wuppertal städte'),
                ('de_kreis', 'de-rp', 'ahrweiler'): ('de_kreis', 'de-rp', 'ahrweiler'),
                ('de_kreis', 'de-rp', 'altenkirchen (westerwald)'): ('de_kreis', 'de-rp', 'altenkirchen'),
                ('de_kreis', 'de-rp', 'alzey-worms'): ('de_kreis', 'de-rp', 'alzey-worms'),
                ('de_kreis', 'de-rp', 'bad dürkheim'): ('de_kreis', 'de-rp', 'bad dürkheim'),
                ('de_kreis', 'de-rp', 'bad kreuznach'): ('de_kreis', 'de-rp', 'bad kreuznach'),
                ('de_kreis', 'de-rp', 'bernkastel-wittlich'): ('de_kreis', 'de-rp', 'bernkastel-wittlich'),
                ('de_kreis', 'de-rp', 'birkenfeld'): ('de_kreis', 'de-rp', 'birkenfeld'),
                ('de_kreis', 'de-rp', 'cochem-zell'): ('de_kreis', 'de-rp', 'cochem-zell'),
                ('de_kreis', 'de-rp', 'donnersbergkreis'): ('de_kreis', 'de-rp', 'donnersbergkreis'),
                ('de_kreis', 'de-rp', 'eifelkreis bitburg-prüm'): ('de_kreis', 'de-rp', 'Bitburg-Prüm'),
                ('de_kreis', 'de-rp', 'frankenthal (pfalz) städte'): ('de_kreis', 'de-rp', 'Frankenthal Städte'),
                ('de_kreis', 'de-rp', 'germersheim'): ('de_kreis', 'de-rp', 'germersheim'),
                ('de_kreis', 'de-rp', 'kaiserslautern'): ('de_kreis', 'de-rp', 'kaiserslautern'),
                ('de_kreis', 'de-rp', 'kaiserslautern städte'): ('de_kreis', 'de-rp', 'kaiserslautern städte'),
                ('de_kreis', 'de-rp', 'koblenz städte'): ('de_kreis', 'de-rp', 'Koblenz Coblenz Städte'),
                ('de_kreis', 'de-rp', 'kusel'): ('de_kreis', 'de-rp', 'kusel'),
                ('de_kreis', 'de-rp', 'landau in der pfalz städte'): ('de_kreis', 'de-rp', 'Landau Städte'),
                ('de_kreis', 'de-rp', 'ludwigshafen am rhein städte'): ('de_kreis', 'de-rp', 'Ludwigshafen Städte'),
                ('de_kreis', 'de-rp', 'mainz städte'): ('de_kreis', 'de-rp', 'mainz städte'),
                ('de_kreis', 'de-rp', 'mainz-bingen'): ('de_kreis', 'de-rp', 'mainz-bingen'),
                ('de_kreis', 'de-rp', 'mayen-koblenz'): ('de_kreis', 'de-rp', 'mayen-koblenz'),
                ('de_kreis', 'de-rp', 'neustadt an der weinstraße städte'): ('de_kreis', 'de-rp', 'Neustadt Städte'),
                ('de_kreis', 'de-rp', 'neuwied'): ('de_kreis', 'de-rp', 'neuwied'),
                ('de_kreis', 'de-rp', 'pirmasens städte'): None,
                ('de_kreis', 'de-rp', 'rhein-hunsrück-kreis'): ('de_kreis', 'de-rp', 'Rhein-Hunsrück'),
                ('de_kreis', 'de-rp', 'rhein-lahn-kreis'): ('de_kreis', 'de-rp', 'Rhein-Lahn'),
                ('de_kreis', 'de-rp', 'rhein-pfalz-kreis'): ('de_kreis', 'de-rp', 'rhein-pfalz-kreis'),
                ('de_kreis', 'de-rp', 'speyer städte'): ('de_kreis', 'de-rp', 'Speyer Spires Städte'),
                ('de_kreis', 'de-rp', 'südliche weinstraße'): ('de_kreis', 'de-rp', 'südliche weinstraße'),
                ('de_kreis', 'de-rp', 'südwestpfalz'): ('de_kreis', 'de-rp', 'südwestpfalz'),
                ('de_kreis', 'de-rp', 'trier städte'): ('de_kreis', 'de-rp', 'trier städte'),
                ('de_kreis', 'de-rp', 'trier-saarburg'): ('de_kreis', 'de-rp', 'trier-saarburg'),
                ('de_kreis', 'de-rp', 'vulkaneifel'): ('de_kreis', 'de-rp', 'vulkaneifel'),
                ('de_kreis', 'de-rp', 'westerwaldkreis'): ('de_kreis', 'de-rp', 'westerwaldkreis'),
                ('de_kreis', 'de-rp', 'worms städte'): ('de_kreis', 'de-rp', 'worms städte'),
                ('de_kreis', 'de-rp', 'zweibrücken städte'): ('de_kreis', 'de-rp', 'zweibrücken städte'),
                ('de_kreis', 'de-sh', 'dithmarschen'): ('de_kreis', 'de-sh', 'dithmarschen'),
                ('de_kreis', 'de-sh', 'flensburg städte'): ('de_kreis', 'de-sh', 'flensburg städte'),
                ('de_kreis', 'de-sh', 'herzogtum lauenburg'): ('de_kreis', 'de-sh', 'Lauenburg'),
                ('de_kreis', 'de-sh', 'kiel städte'): ('de_kreis', 'de-sh', 'kiel städte'),
                ('de_kreis', 'de-sh', 'lübeck städte'): ('de_kreis', 'de-sh', 'lübeck städte'),
                ('de_kreis', 'de-sh', 'neumünster städte'): ('de_kreis', 'de-sh', 'neumünster städte'),
                ('de_kreis', 'de-sh', 'nordfriesland'): ('de_kreis', 'de-sh', 'nordfriesland'),
                ('de_kreis', 'de-sh', 'ostholstein'): ('de_kreis', 'de-sh', 'ostholstein'),
                ('de_kreis', 'de-sh', 'pinneberg'): ('de_kreis', 'de-sh', 'pinneberg'),
                ('de_kreis', 'de-sh', 'plön'): ('de_kreis', 'de-sh', 'plön'),
                ('de_kreis', 'de-sh', 'rendsburg-eckernförde'): ('de_kreis', 'de-sh', 'rendsburg-eckernförde'),
                ('de_kreis', 'de-sh', 'schleswig-flensburg'): ('de_kreis', 'de-sh', 'schleswig-flensburg'),
                ('de_kreis', 'de-sh', 'segeberg'): ('de_kreis', 'de-sh', 'segeberg'),
                ('de_kreis', 'de-sh', 'steinburg'): ('de_kreis', 'de-sh', 'steinburg'),
                ('de_kreis', 'de-sh', 'stormarn'): ('de_kreis', 'de-sh', 'stormarn'),
                ('de_kreis', 'de-sl', 'merzig-wadern'): ('de_kreis', 'de-sl', 'merzig-wadern'),
                ('de_kreis', 'de-sl', 'neunkirchen'): ('de_kreis', 'de-sl', 'neunkirchen'),
                ('de_kreis', 'de-sl', 'regionalverband saarbrücken'): ('de_kreis', 'de-sl', 'Saarbrücken Städte'),
                ('de_kreis', 'de-sl', 'saarlouis'): ('de_kreis', 'de-sl', 'saarlouis'),
                ('de_kreis', 'de-sl', 'saarpfalz-kreis'): ('de_kreis', 'de-sl', 'Saarpfalz'),
                ('de_kreis', 'de-sl', 'st. wendel'): ('de_kreis', 'de-sl', 'Sankt Wendel'),
                ('de_kreis', 'de-sn', 'bautzen'): ('de_kreis', 'de-sn', 'bautzen'),
                ('de_kreis', 'de-sn', 'chemnitz städte'): ('de_kreis', 'de-sn', 'chemnitz städte'),
                ('de_kreis', 'de-sn', 'dresden städte'): ('de_kreis', 'de-sn', 'dresden städte'),
                ('de_kreis', 'de-sn', 'erzgebirgskreis'): ('de_kreis', 'de-sn', 'Mittlerer Erzgebirgskreis'),
                ('de_kreis', 'de-sn', 'görlitz'): ('de_kreis', 'de-sn', 'Görlitz Städte'),
                ('de_kreis', 'de-sn', 'leipzig'): ('de_kreis', 'de-sn', 'Leipziger Land'),
                ('de_kreis', 'de-sn', 'leipzig städte'): ('de_kreis', 'de-sn', 'leipzig städte'),
                ('de_kreis', 'de-sn', 'meißen'): ('de_kreis', 'de-sn', 'meißen'),
                ('de_kreis', 'de-sn', 'mittelsachsen'): None,
                ('de_kreis', 'de-sn', 'nordsachsen'): None,
                ('de_kreis', 'de-sn', 'sächsische schweiz-osterzgebirge'): ('de_kreis', 'de-sn', 'Sächsische Schweiz'),
                ('de_kreis', 'de-sn', 'vogtlandkreis'): ('de_kreis', 'de-sn', 'vogtlandkreis'),
                ('de_kreis', 'de-sn', 'zwickau'): ('de_kreis', 'de-sn', 'Zwickau Städte'),
                ('de_kreis', 'de-st', 'altmarkkreis salzwedel'): ('de_kreis', 'de-st', 'altmarkkreis salzwedel'),
                ('de_kreis', 'de-st', 'anhalt-bitterfeld'): ('de_kreis', 'de-st', 'Bitterfeld'),
                ('de_kreis', 'de-st', 'burgenlandkreis'): ('de_kreis', 'de-st', 'burgenlandkreis'),
                ('de_kreis', 'de-st', 'börde'): ('de_kreis', 'de-st', 'Bördekreis'),
                ('de_kreis', 'de-st', 'dessau-roßlau städte'): ('de_kreis', 'de-st', 'Dessau Städte'),
                ('de_kreis', 'de-st', 'halle (saale) städte'): ('de_kreis', 'de-st', 'Halle Städte'),
                ('de_kreis', 'de-st', 'harz'): None, #('de_kreis', 'de-st', 'Osterode'),
                ('de_kreis', 'de-st', 'jerichower land'): ('de_kreis', 'de-st', 'jerichower land'),
                ('de_kreis', 'de-st', 'magdeburg städte'): ('de_kreis', 'de-st', 'magdeburg städte'),
                ('de_kreis', 'de-st', 'mansfeld-südharz'): ('de_kreis', 'de-st', 'Mansfelder Land'),
                ('de_kreis', 'de-st', 'saalekreis'): ('de_kreis', 'de-st', 'Halle Städte'),
                ('de_kreis', 'de-st', 'salzlandkreis'): None,
                ('de_kreis', 'de-st', 'stendal'): ('de_kreis', 'de-st', 'stendal'),
                ('de_kreis', 'de-st', 'wittenberg'): ('de_kreis', 'de-st', 'wittenberg'),
                ('de_kreis', 'de-th', 'altenburger land'): ('de_kreis', 'de-th', 'altenburger land'),
                ('de_kreis', 'de-th', 'eichsfeld'): ('de_kreis', 'de-th', 'eichsfeld'),
                ('de_kreis', 'de-th', 'eisenach städte'): None,
                ('de_kreis', 'de-th', 'erfurt städte'): ('de_kreis', 'de-th', 'erfurt städte'),
                ('de_kreis', 'de-th', 'gera städte'): ('de_kreis', 'de-th', 'gera städte'),
                ('de_kreis', 'de-th', 'gotha'): ('de_kreis', 'de-th', 'gotha'),
                ('de_kreis', 'de-th', 'greiz'): ('de_kreis', 'de-th', 'greiz'),
                ('de_kreis', 'de-th', 'hildburghausen'): ('de_kreis', 'de-th', 'hildburghausen'),
                ('de_kreis', 'de-th', 'ilm-kreis'): ('de_kreis', 'de-th', 'ilm-kreis'),
                ('de_kreis', 'de-th', 'jena städte'): ('de_kreis', 'de-th', 'jena städte'),
                ('de_kreis', 'de-th', 'kyffhäuserkreis'): ('de_kreis', 'de-th', 'kyffhäuserkreis'),
                ('de_kreis', 'de-th', 'nordhausen'): ('de_kreis', 'de-th', 'nordhausen'),
                ('de_kreis', 'de-th', 'saale-holzland-kreis'): ('de_kreis', 'de-th', 'Saale-Holzland'),
                ('de_kreis', 'de-th', 'saale-orla-kreis'): ('de_kreis', 'de-th', 'Saale-Orla'),
                ('de_kreis', 'de-th', 'saalfeld-rudolstadt'): ('de_kreis', 'de-th', 'saalfeld-rudolstadt'),
                ('de_kreis', 'de-th', 'schmalkalden-meiningen'): ('de_kreis', 'de-th', 'schmalkalden-meiningen'),
                ('de_kreis', 'de-th', 'sonneberg'): ('de_kreis', 'de-th', 'sonneberg'),
                ('de_kreis', 'de-th', 'suhl städte'): ('de_kreis', 'de-th', 'suhl städte'),
                ('de_kreis', 'de-th', 'sömmerda'): ('de_kreis', 'de-th', 'sömmerda'),
                ('de_kreis', 'de-th', 'unstrut-hainich-kreis'): ('de_kreis', 'de-th', 'Unstrut-Hainich'),
                ('de_kreis', 'de-th', 'wartburgkreis'): ('de_kreis', 'de-th', 'wartburgkreis'),
                ('de_kreis', 'de-th', 'weimar städte'): ('de_kreis', 'de-th', 'weimar städte'),
                ('de_kreis', 'de-th', 'weimarer land'): ('de_kreis', 'de-th', 'weimarer land')
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_kreis_2_data())
        return r

    def _get_kreis_2_data(self):
        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()
            path = f'{base_dir}/{date}/kreis.json'

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

            for feature in data['features']:
                attributes = feature['attributes']
                #print(attributes)

                # Only confirmed and deaths are shown in the dashboard
                date = self.convert_date(
                    attributes['last_update'].split()[0]
                                             .strip(',')
                                             .replace('.', '/')
                )
                region_parent = name_to_state[attributes['BL'].lower()]
                region_child = attributes['GEN']
                confirmed = attributes['cases']
                deaths = attributes['deaths']
                recovered = attributes['recovered']

                if 'stadt' in attributes['BEZ'].lower():
                    #print(attributes)
                    region_child += ' Städte'

                if confirmed is not None:
                    r.append(
                        region_schema=Schemas.DE_KREIS,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if deaths is not None:
                    r.append(
                        region_schema=Schemas.DE_KREIS,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if recovered is not None:
                    r.append(
                        region_schema=Schemas.DE_KREIS,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if recovered is not None and confirmed is not None and deaths is not None:
                    r.append(
                        region_schema=Schemas.DE_KREIS,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(confirmed)-int(recovered)-int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

            out.extend(r)
        return out


if __name__ == '__main__':
    from pprint import pprint
    from covid_19_au_grab.datatypes.datapoints_thinned_out import datapoints_thinned_out
    inst = DERKIData()
    datapoints = inst.get_datapoints()
    #inst.sdpf.print_mappings()
    pprint(datapoints)
