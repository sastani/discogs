/* DDL FOR artist entities*/
CREATE TABLE artist(
    id INT PRIMARY KEY,
    artist_name VARCHAR,
    name VARCHAR,
    profile VARCHAR,
    data_quality VARCHAR
);

CREATE TABLE artist_name_variations(
    artist_id INT,
    name VARCHAR,
    PRIMARY KEY(artist_id, name)
);

CREATE TABLE artist_aliases(
    artist_id INT,
    alias_artist_id INT,
    alias_name VARCHAR,
    PRIMARY KEY(artist_id, alias_artist_id)
);

CREATE TABLE artist_groups(
    artist_id INT,
    group_artist_id INT,
    group_name VARCHAR
)

CREATE TABLE artist_urls(
    artist_id INT,
    url VARCHAR,
    page_type VARCHAR,
    PRIMARY KEY(artist_id, url)
);


/* DDL FOR label entities*/
CREATE TABLE label(
    id INT PRIMARY KEY,
    name VARCHAR,
    parent_label_id INT,
    parent_label_name VARCHAR,
    contact_info VARCHAR,
    profile VARCHAR,
    data_quality VARCHAR
);


CREATE TABLE label_sublabels(
    label_id INT NOT NULL,
    sublabel_label_id INT NOT NULL,
    sublabel_label_name VARCHAR,
    PRIMARY KEY (label_id, sublabel_label_id)
);

CREATE TABLE label_urls(
    label_id INT references label(id),
    url VARCHAR,
    page_type VARCHAR,
    PRIMARY KEY(label_id, url)
);


/* DDL FOR release entities*/
CREATE TABLE release
(
    id INT PRIMARY KEY,
    title VARCHAR NOT NULL,
    country VARCHAR,
    release_year INT,
    release_month INT,
    release_day INT,
    released_string VARCHAR,
    status VARCHAR,
    data_quality VARCHAR
);

CREATE TABLE release_artists
(
    release_id  INT,
    artist_id   INT,
    artist_name VARCHAR,
    ordinal INT,
    join_string VARCHAR
);

CREATE TABLE release_genres
(
    release_id INT,
    genre VARCHAR,
    PRIMARY KEY (release_id, genre)
);

CREATE TABLE release_styles
(
    release_id INT,
    style VARCHAR
);

CREATE TABLE release_tracks
(
    release_id INT,
    track_title VARCHAR,
    track_number INT,
    position VARCHAR,
    duration  TIME,
    duration_string VARCHAR
);

CREATE TABLE release_labels
(
    release_id INT,
    label_id INT,
    label_name VARCHAR,
    catalog_nums VARCHAR[]
);

CREATE TABLE release_formats
(
    release_id INT references release(id),
    format VARCHAR,
    quantity_string VARCHAR,
    text VARCHAR,
    description_arr VARCHAR[]
);

/*DDL for release to master release entities*/
CREATE TABLE release_master
(
    release_id INT PRIMARY KEY,
    master_id INT,
    is_main_release BOOLEAN
);
