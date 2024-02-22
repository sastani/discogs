CREATE INDEX artists_name_idx ON artists(name);
CREATE INDEX artists_artist_name_idx ON artists(artist_name);
CREATE INDEX artist_aliases_alias_name_idx ON artist_aliases(alias_name);
--
CREATE INDEX labels_label_name_idx ON labels(label_name);
CREATE INDEX label_sub_labels_sub_label_name_idx ON label_sub_labels(sub_label_name);
--
CREATE INDEX releases_title_idx ON releases(title);
CREATE INDEX releases_release_date_idx ON releases(release_date);
CREATE INDEX releases_label_name_idx ON releases(label_name);
CREATE INDEX release_genres_genre_idx ON release_genres(genre);
CREATE INDEX release_styles_style_idx ON release_styles(style);