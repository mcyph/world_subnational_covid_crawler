PRAGMA ENCODING = "UTF-8";

-- Increase performance in trade for lower integrity.
--
-- Because we're copying the DB file for each revision,
-- we'll still be able to roll back to a previous
-- SQLite file in the case of power failure, etc.

PRAGMA SYNCHRONOUS = 0;
PRAGMA JOURNAL_MODE = OFF;

-- --------------------------- --
--         DataPoints          --
-- --------------------------- --

CREATE TABLE datapoints (
    date_updated CHAR(10),
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),
    agerange VARCHAR(16),
    datatype VARCHAR(32),
    `value` BIGINT,
    source_url_id BIGINT NOT NULL,
    text_match VARCHAR(512),

    -- values scraped from Australian state news releases
    -- sometimes contain errors. This makes sure the values
    -- can be checked before they go live.
    -- Both these will be NULL unless explicitly set.
    datetime_confirmed TIMESTAMP,
    confirmed_uid VARCHAR(32),

    is_derived SMALLINT NOT NULL,
    date_inserted TIMESTAMP NOT NULL
);

CREATE INDEX datapoints_idx1 ON datapoints (
    date_updated,
    region_schema, region_parent, region_child,
    agerange, datatype,
    `value`
);

CREATE INDEX datapoints_idx2 ON datapoints (
    region_schema, region_parent, region_child,
    date_updated,
    agerange, datatype,
    `value`
);

-- -------------- --
-- Source URL IDs --
-- -------------- --

CREATE TABLE sourceurls (
    -- The table which allows getting the most recent
    -- revision, and the status of that run as a
    -- '{"key": ["OK"/"Error", message]}' JSON string
    source_url_id BIGINT NOT NULL PRIMARY KEY,
    source_url TEXT NOT NULL UNIQUE
);
