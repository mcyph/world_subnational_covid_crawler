PRAGMA ENCODING = "UTF-8";

-- Increase performance in trade for lower integrity.
--
-- Because we're copying the DB file for each revision,
-- we'll still be able to roll back to a previous
-- SQLite file in the case of power failure, etc.

-- PRAGMA JOURNAL_MODE = WAL;
PRAGMA JOURNAL_MODE = OFF;
PRAGMA SYNCHRONOUS = OFF;
PRAGMA LOCKING_MODE = EXCLUSIVE;

-- --------------------------- --
--         DataPoints          --
-- --------------------------- --

CREATE TABLE datapoints (
    date_updated CHAR(10),
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),
    datatype VARCHAR(32),
    agerange VARCHAR(16),
    `value` BIGINT,
    source_url_id BIGINT NOT NULL,
    text_match VARCHAR(512),

    is_derived SMALLINT NOT NULL,
    date_inserted TIMESTAMP NOT NULL,

    source_id CHAR(32) NOT NULL
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
