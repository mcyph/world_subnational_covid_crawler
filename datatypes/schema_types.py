import json
from covid_19_au_grab.get_package_dir import get_package_dir


with open(get_package_dir() / 'datatypes' / 'schema_types.json',
          'r', encoding='utf-8') as f:
    schema_types = json.loads(f.read())

