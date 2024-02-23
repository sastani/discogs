import psycopg
from psycopg import sql
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DB")

#table name and column/attributes for each table
artist = \
    {
        "artists": ["artist_id", "artist_name", "name", "profile", "data_quality"],
        "artist_name_variations": ["artist_id", "name"],
        "artist_aliases": ["artist_id", "alias_id", "alias_name"],
        "artist_urls": ["artist_id", "url", "page_type"],
    }
label = \
    {
        "labels": ["label_id", "label_name", "parent_label_id", "parent_label_name", "contact_info", "profile",
                   "data_quality"],
        "label_sub_labels": ["label_id", "sub_label_id", "sub_label_name"],
        "label_urls": ["label_id", "url", "page_type"]
    }
release =\
    {
        "releases": ["release_id", "master_id", "title", "release_date", "label_id", "label_name", "status", "data_quality"],
        "release_artists": ["release_id", "artist_id", "artist_name", "ordinal", "join_string"],
        "release_genres": ["release_id", "genre"],
        "release_styles": ["release_id", "style"],
        "release_tracks": ["release_id", "track_title", "track_number", "duration"],
        "release_labels": ["release_id", "label_id", "label_name", "catalog_num"],
        "release_formats": ["release_id", "format", "quantity", "description_arr"],
        "master_releases": ["master_id", "release_id"],
        "master_main_release": ["master_id", "release_id"]
    }
all_tables = [artist, label, release]

class Exporter:
    def __init__(self):
        self.conn = psycopg.connect(user = user, password=password,
                                    host=host, port=port, dbname=database)
        self.cur = self.conn.cursor()

    def batch_insert(self, table_name, q):
        for related_tables in all_tables:
            for table, cols in related_tables.items():
                query = 'INSERT INTO {table} VALUES (%s), '.format(table=sql.Identifier(table_name))







