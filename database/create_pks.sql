--might fail due to discogs duplicates
ALTER TABLE release_artists ADD CONSTRAINT release_artists_pk PRIMARY KEY (release_id, artist_id, ordinal);
ALTER TABLE release_tracks ADD CONSTRAINT release_tracks_pk PRIMARY KEY(release_id, track_title, track_number);
ALTER TABLE release_labels ADD CONSTRAINT release_labels_pk PRIMARY KEY(release_id, label_id);

--will very likely fail (almost 100%)
ALTER TABLE release_styles ADD CONSTRAINT release_styles_pk PRIMARY KEY (release_id, style);
ALTER TABLE release_formats ADD CONSTRAINT release_formats_pk PRIMARY KEY (release_id, format, text, description_arr);

--ALTER TABLE label_sublabels ADD CONSTRAINT label_sublabels_pk PRIMARY KEY()

