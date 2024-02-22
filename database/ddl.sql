/* DDL FOR artist entities*/
CREATE TABLE artists(
    artist_id INT PRIMARY KEY NOT NULL,
    artist_name VARCHAR,
    name VARCHAR,
    profile VARCHAR,
    data_quality VARCHAR
);

CREATE TABLE artist_name_variations(
    artist_id INT references artists(artist_id),
    name VARCHAR,
    PRIMARY KEY(artist_id, name)
);

CREATE TABLE artist_aliases(
    artist_id INT references artists(artist_id),
    alias_id INT references artists(artist_id),
    alias_name VARCHAR,
    PRIMARY KEY(artist_id, alias_id)
);


/* DDL FOR label entities*/
CREATE TABLE labels(
    label_id INT PRIMARY KEY NOT NULL,
    parent_label_id INT,
    parent_label_name VARCHAR,
    label_name VARCHAR,
    contact_info VARCHAR,
    profile VARCHAR,
    data_quality VARCHAR
);


CREATE TABLE label_sub_labels(
    label_id INT references labels(label_id),
    sub_label_id INT references labels(label_id),
    sub_label_name VARCHAR
);

/* DDL FOR release entities*/
CREATE TABLE releases
(
    release_id INT PRIMARY KEY NOT NULL,
    master_id INT,
    title VARCHAR NOT NULL,
    release_date DATE,
    label_id INT,
    label_name VARCHAR,
    status VARCHAR,
    data_quality VARCHAR
);

CREATE TABLE release_artists
(
    release_id  INT references releases (release_id),
    artist_id   INT references artists (artist_id),
    artist_name VARCHAR,
    join_string VARCHAR
);

CREATE TABLE release_styles
(
    release_id INT references releases(release_id),
    style VARCHAR,
    PRIMARY KEY (release_id, style)
);

CREATE TABLE release_tracks
(
    release_id INT references releases(release_id),
    track_title VARCHAR,
    position INT,
    duration  TIME,
    PRIMARY KEY(release_id, track_title)
);

CREATE TABLE release_labels
(
    release_id INT references releases(release_id),
    label_id INT references labels(label_id),
    label_name VARCHAR,
    catalog_num VARCHAR
);

CREATE TABLE release_formats
(
    release_id INT references releases(release_id),
    format VARCHAR,
    quantity INT,
    description VARCHAR,
    PRIMARY KEY(release_id, format)
);