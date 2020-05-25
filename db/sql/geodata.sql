CREATE TABLE geodata_schema (
    region_schema VARCHAR(32),
    description VARCHAR(8192),
    priority NUMBER,
    minzoom DOUBLE,
    maxzoom DOUBLE,
    replaces_schema VARCHAR(64),
    replaces_parent VARCHAR(64),
    replaces_child VARCHAR(64)
) collate utf8_bin;

CREATE TABLE geodata_poly (
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),
    iso3166_2 VARCHAR(32),
    native_name VARCHAR(64),
    population BIGINT,
    centre_latlong POINT,
    extent_latlong POLYGON,
    polygons MULTIPOLYGON
) collate utf8_bin;

CREATE TABLE geodata_trans (
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),
    bcp47 VARCHAR(64),
    parent_trans VARCHAR(64),
    child_trans VARCHAR(64)
) collate utf8_bin;
