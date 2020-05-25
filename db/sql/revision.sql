CREATE TABLE revision (
    confirmed SMALLINT,
    revision_id BIGINT,
    date_updated CHAR(10),
    region_schema VARCHAR(32),
    region_parent VARCHAR(64),
    region_child VARCHAR(64),
    agerange VARCHAR(16),
    datatype VARCHAR(32),
    value BIGINT,
    source_url VARCHAR(8192),
    text_match VARCHAR(2048),
    datetime_added DATE,
    user_id VARCHAR(64)
) collate utf8_bin;

CREATE TABLE revision_id (
    revision_id BIGINT,
    revision_datetime DATE,
    status_json BIGBLOB
) collate utf8_bin;
