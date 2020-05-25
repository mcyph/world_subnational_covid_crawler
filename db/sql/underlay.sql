-- ------------------------------------------------------ --
-- Other Values which can be Underlayed under the GeoData --
-- ------------------------------------------------------ --

CREATE TABLE underlay_key (
    underlay_key VARCHAR(128) NOT NULL,
    underlay_group VARCHAR(128) NOT NULL,


    region_schema VARCHAR(32) NOT NULL,
    description VARCHAR(128),
    source_url VARCHAR(2048),
    license VARCHAR(128),

    -- Optional PNG data for the marker
    -- (if using underlay points)
    marker_data BLOB
) collate utf8_bin;

CREATE UNIQUE INDEX underlay_key_idx1 ON underlay_key (
    underlay_key
);

-- -------------------------------------------------------- --
-- Underlay Data Values (Corresponding to a GeoData Schema) --
-- -------------------------------------------------------- --

-- This is useful for adding a background colour

CREATE TABLE underlay_value (
    -- The region
    underlay_key VARCHAR(128) NOT NULL,

    -- Which values in the underlay
    -- this value corresponds to
    region_parent VARCHAR(64),
    region_child VARCHAR(64),

    -- This can be either NULL, or be a "YYYY_MM_DD"-format
    -- date, allowing for timeseries data
    date_updated CHAR(10),

    -- Either an int or a float value
    -- can be used, not both.
    value_int BIGINT,
    value_float DOUBLE,

    -- Any extra data, such as an explanation or something
    -- else that could be rendered with additional logic,
    -- can be put in the JSON metadata
    metadata_json BLOB
) collate utf8_bin;

CREATE UNIQUE INDEX underlay_value_idx1 ON underlay_value (
    underlay_key, region_parent, region_child, date_updated
);

-- ------------------------------------------------------------- --
-- Underlay Data Values (Corresponding to Specific Areas/Points) --
-- ------------------------------------------------------------- --

-- This could be useful for specific airports, etc
-- which a marker could be placed on

CREATE TABLE underlay_point (
    underlay_key VARCHAR(128),
    date_updated CHAR(10),

    -- The centre point/multipolygons
    -- this place corresponds to.
    -- Can be one or the other, or both.
    centre_point POINT,   -- TODO: Should different marker types be supported?? ====================================
    polygons MULTIPOLYGON,

    -- One or the other is allowed,
    -- as in underlay_value
    value_int BIGINT,
    value_float DOUBLE,

    -- Extra data
    metadata_json BLOB
) collate utf8_bin;

CREATE INDEX underlay_point_idx1 ON underlay_point (
    underlay_key, date_updated
);
