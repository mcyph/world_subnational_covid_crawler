-- ------------ --
-- Revision IDs --
-- ------------ --

CREATE TABLE revision_id (
    -- The table which allows getting the most recent
    -- revision, and the status of that run as a
    -- '{"key": ["OK"/"Error", message]}' JSON string
    revision_id BIGINT NOT NULL PRIMARY KEY,
    revision_datetime DATE NOT NULL,
    status_json BLOB NOT NULL
) collate utf8_bin;

CREATE INDEX revision_id_idx2 ON revision_id (
    revision_datetime
);

-- -------- --
-- Revision --
-- -------- --

CREATE TABLE revision (
    -- date_updated is in format YYYY_MM_DD so as to allow
    -- for binary sorting.
    revision_id BIGINT NOT NULL,
    date_updated CHAR(10) NOT NULL,

    -- Applies to region (e.g. if region_schema is admin1,
    -- iso3166-1 code for region_parent and iso3166-2 code
    -- for region_child is expected.
    -- region_parent is expected to be NULL for admin0
    -- (country level), and is optional for other schemas;
    -- region_child is always required.
    region_schema VARCHAR(32) NOT NULL,
    region_parent VARCHAR(64),
    region_child VARCHAR(64) NOT NULL,

    -- The age range the value applies to (e.g. "0-9" or "90+")
    -- the datatype (e.g. "total") and the integer value.
    -- (I can't think of any cases where covid 19 stat values
    --  would be given as floats, except as per-capita counts,
    --  but they should be calculated on-the-fly using
    -- `population` in `geodata_poly`.
    agerange VARCHAR(16),
    datatype VARCHAR(32),
    value BIGINT NOT NULL,

    -- Source information
    source_url VARCHAR(8192) NOT NULL,
    text_match VARCHAR(2048),
    user_id VARCHAR(64)
) collate utf8_bin;

CREATE UNIQUE INDEX revision_idx1 ON revision (
    revision_id, date_updated,
    region_schema, region_parent, region_child,
    agerange, datatype
);

-- --------------------------- --
-- Confirmed (Verified) Values --
-- --------------------------- --

-- values scraped from Australian state news releases
-- sometimes contain errors. This makes sure the values
-- can be checked before they go live.

CREATE TABLE confirmed (
    date_updated CHAR(10),
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),
    agerange VARCHAR(16),
    datatype VARCHAR(32),
    value BIGINT,
    datetime_confirmed DATE,
    confirmed_uid VARCHAR(32)
) collate utf8_bin;

CREATE UNIQUE INDEX confirmed_idx1 ON confirmed (
    date_updated,
    region_schema, region_parent, region_child,
    agerange, datatype,
    value
);
