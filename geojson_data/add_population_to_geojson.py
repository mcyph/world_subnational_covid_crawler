from pathlib import Path
from collections import Counter

import rasterio
import rasterio.mask
import geopandas as gpd
from shapely.geometry import mapping


# Population data from https://www.worldpop.org/project/categories?id=3
POP_PATH = '/home/david/Downloads/ppp_2020_1km_Aggregated.tif'
data = rasterio.open(POP_PATH)


def get_pop(geometry):
    clipped_array, clipped_transform = rasterio.mask.mask(
        data, [mapping(geometry)], crop=True, nodata=-999999
    )
    #show(clipped_array, cmap='terrain')

    i = 0
    for X in clipped_array:
        for y in X:
            for z in y:
                if int(z) != -999999:
                    i += z
    return i


out = Counter()
ok_indicator = {}

base_path = Path('/home/david/dev/global_subnational_covid_data/geojson/poly/')
for path in base_path.iterdir():
    df = gpd.read_file(path)

    for item in df.iloc:
        try:
            out[item.region_schema, item.region_parent, item.region_child] += get_pop(item.geometry)
            ok_indicator.setdefault((item.region_schema, item.region_parent, item.region_child), True)
        except ValueError:
            import traceback
            traceback.print_exc()
            ok_indicator[item.region_schema, item.region_parent, item.region_child] = False

print()
print('region_schema\tregion_parent\tregion_child\tpop_2020\tno_exc')
for (region_schema, region_parent, region_child), pop in sorted(out.items()):
    print(f'{region_schema}\t'
          f'{region_parent}\t'
          f'{region_child}\t'
          f'{round(pop)}\t'
          f'{ok_indicator[region_schema, region_parent, region_child]}')
