import json
from covid_19_au_grab._utility.get_package_dir import get_package_dir


with open(get_package_dir() / 'covid_db' / 'datatypes' / 'schema_types.json',
          'r', encoding='utf-8') as f:
    schema_types = json.loads(f.read())

