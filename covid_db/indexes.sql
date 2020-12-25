CREATE INDEX datapoints_idx1 ON datapoints (
    date_updated,
    region_schema, region_parent, region_child,
    datatype, agerange,
    `value`
);

CREATE INDEX datapoints_idx2 ON datapoints (
    region_schema, region_parent, region_child,
    date_updated,
    datatype, agerange,
    `value`
);

CREATE INDEX datapoints_idx3 ON datapoints (
    source_id, datatype, date_updated
);

CREATE INDEX datapoints_idx4 ON datapoints (
    -- For querying+outputting
    region_schema, datatype, region_parent, region_child
);
