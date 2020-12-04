import json
from covid_crawlers.oceania.au_data.nsw.NSWJSONOpenData import NSWJSONOpenData, POSTCODE_TO_LGA

NSWJSONOpenData().get_datapoints()

with open('postcode_to_lga.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(POSTCODE_TO_LGA))
