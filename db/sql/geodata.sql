-- --------------------------------- --
-- Polygons Corresponding to Regions --
-- --------------------------------- --

CREATE TABLE geodata_schema (
    -- Schema could be admin0 for iso3166-1 (country) values
    -- or admin1 for iso3166-2 (country and state or territory),
    -- or a custom scheme. admin0/admin1 are preferred over
    -- custom schemes due to having a lot of permissive data
    -- which also includes much translation data.
    region_schema VARCHAR(32) NOT NULL PRIMARY KEY,

    -- A text description for the schema
    -- (e.g. explaining what LGA stands for, etc)
    description VARCHAR(8192),

    -- Higher numbers take precedence if there's data available
    -- for two schemas replacing the same parent/child
    priority NUMBER,

    -- Optional: the zoom levels from/to this will be displayed
    minzoom DOUBLE,
    maxzoom DOUBLE,

    -- A schema can optionally replace an element from another.
    -- For example, LHD could replace Australia/NSW with itself,
    -- or LGA could replace the entire of Australia.
    -- If there's more than one possibility for a given set of
    -- time series data, schemas with a higher `priority`
    -- will take precedence.
    replaces_schema VARCHAR(64),
    replaces_parent VARCHAR(64),
    replaces_child VARCHAR(64)
) collate utf8_bin;

-- --------------------------------- --
-- Polygons Corresponding to Regions --
-- --------------------------------- --

-- TODO: Add support for higher quality poly's at higher zoom levels!!! ================================================

CREATE TABLE geodata_poly (
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),

    -- The name of the region in the most-used language of the country
    native_name VARCHAR(64),

    -- The population of the region - useful for per-capita calculations
    population BIGINT,

    -- Either an automatically-calculated centre point for the region
    -- using polyfill.js, if one is supplied by the datasource
    centre_latlong POINT NOT NULL,
    extent_latlong POLYGON,

    -- The polygons corresponding to this item
    -- TODO: Would it be faster to use POLYGON's in a separate table?? =================================================
    polygons MULTIPOLYGON
) collate utf8_bin;

CREATE UNIQUE INDEX geodata_poly_idx1 ON geodata_poly (
    region_schema, region_parent, region_child
);

CREATE SPATIAL INDEX geodata_poly_idx2 ON revision (
    polygons  --  CHECK ME!!! ==========================================================================================
);

-- ---------------------------- --
-- Translations for Place Names --
-- ---------------------------- --

-- This provides a basic system for translations. Mainly
-- uses data from the Unicode CLDR subdivision names e.g. at
-- https://unicode-org.github.io/cldr-staging/charts/37/subdivisionNames

CREATE TABLE geodata_trans (
    -- The schema/parent/child "key"
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),

    -- The IETF language code:
    -- https://tools.ietf.org/html/bcp47
    bcp47 VARCHAR(64),

    -- The translations themselves
    parent_trans VARCHAR(64),
    child_trans VARCHAR(64)
) collate utf8_bin;

CREATE UNIQUE INDEX geodata_trans_idx1 ON geodata_trans (
    region_schema, region_parent, region_child,
    bcp47
);
