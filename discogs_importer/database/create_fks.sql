--artists
ALTER TABLE artist_name_variations ADD CONSTRAINT artist_name_variations_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id);

ALTER TABLE artist_aliases ADD CONSTRAINT artist_aliases_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id);
ALTER TABLE artist_aliases ADD CONSTRAINT artist_aliases_alias_artist_fk FOREIGN KEY (alias_artist_id) REFERENCES artist(id);

ALTER TABLE artist_groups ADD CONSTRAINT artist_groups_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id);
ALTER TABLE artist_groups ADD CONSTRAINT artist_groups_name_fk FOREIGN KEY (artist_name) REFERENCES artist(artist_name);
ALTER TABLE artist_groups ADD CONSTRAINT artist_groups_group_fk FOREIGN KEY (group_artist_id) REFERENCES artist(id);
ALTER TABLE artist_groups ADD CONSTRAINT artist_groups_group_name_fk FOREIGN KEY (group_name) REFERENCES artist(artist_name);

ALTER TABLE artist_urls ADD CONSTRAINT artist_urls_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id);

--labels
ALTER TABLE label_sublabels ADD CONSTRAINT label_sublabels_label_fk FOREIGN KEY (label_id) REFERENCES label(id);
ALTER TABLE label_sublabels ADD CONSTRAINT label_sublabels_sublabel_fk FOREIGN KEY (sublabel_label_id) REFERENCES label(id);
ALTER TABLE label_sublabels ADD CONSTRAINT label_sublabels_sublabel_name_fk FOREIGN KEY (sublabel_label_name) REFERENCES label(name)

ALTER TABLE label_urls ADD CONSTRAINT label_urls_label_fk FOREIGN KEY (label_id) REFERENCES label(id);

--releases
ALTER TABLE release_artists ADD CONSTRAINT release_artists_release_fk FOREIGN KEY (release_id) REFERENCES release(id);
ALTER TABLE release_artists ADD CONSTRAINT release_artists_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id);
ALTER TABLE release_genres ADD CONSTRAINT release_genres_release_fk FOREIGN KEY (release_id) REFERENCES release(id);
ALTER TABLE release_styles ADD CONSTRAINT release_styles_release_fk FOREIGN KEY (release_id) REFERENCES release(id);
ALTER TABLE release_tracks ADD CONSTRAINT release_tracks_release_fk FOREIGN KEY (release_id) REFERENCES release(id);
ALTER TABLE release_labels ADD CONSTRAINT release_labels_release_fk FOREIGN KEY (release_id) REFERENCES release(id);
ALTER TABLE release_formats ADD CONSTRAINT release_formats_release_fk FOREIGN KEY (release_id) REFERENCES release(id);
ALTER TABLE release_master ADD CONSTRAINT release_master_release_fk FOREIGN KEY (release_id) REFERENCES release(id);


