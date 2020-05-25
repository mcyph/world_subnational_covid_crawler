CREATE TABLE underlay_key (
    underlay_key VARCHAR(128),
    underlay_group VARCHAR(128),
    region_schema VARCHAR(32),
    description VARCHAR(128),
    source_url VARCHAR(2048),
    license VARCHAR(128)
) collate utf8_bin;

CREATE INDEX underlay_key_idx1

CREATE TABLE underlay_value (
    underlay_key VARCHAR(128),
    underlay_parent VARCHAR(64),
    underlay_child VARCHAR(64),
    date_updated CHAR(10),
    value_int BIGINT,
    value_float DOUBLE,
    metadata_json BIGBLOB
) collate utf8_bin;

CREATE TABLE underlay_point (
    underlay_key VARCHAR(128),
    date_updated CHAR(10),
    centre_point POINT,
    polygons POLYGON,
    value_int BIGINT,
    value_float DOUBLE,
    metadata_json BIGBLOB
) collate utf8_bin;
