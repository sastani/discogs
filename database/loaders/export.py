import psycopg
from psycopg import sql
import os
from dotenv import load_dotenv
from collections import deque
from models.release import Release

load_dotenv()
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DB")

#table name and column/attributes for each table
artist = \
    {
        "artists": ["id", "artist_name", "name", "profile", "data_quality"],
        "artist_name_variations": ["artist_id", "name"],
        "artist_aliases": ["artist_id", "alias_id", "alias_name"],
        "artist_urls": ["artist_id", "url", "page_type"],
    }
label = \
    {
        "labels": ["id", "label_name", "parent_label_id", "parent_label_name", "contact_info", "profile",
                   "data_quality"],
        "label_sub_labels": ["label_id", "sub_label_id", "sub_label_name"],
        "label_urls": ["label_id", "url", "page_type"]
    }
release =\
    {
        "releases": ["id", "title", "country", "release_year", "release_month", "release_day", "status", "data_quality"],
        "release_artists": ["release_id", "artist_id", "artist_name", "ordinal", "join_string"],
        "release_genres": ["release_id", "genre"],
        "release_styles": ["release_id", "style"],
        "release_tracks": ["release_id", "track_title", "track_number", "position", "duration"],
        "release_labels": ["release_id", "label_id", "label_name", "catalog_nums"],
        "release_formats": ["release_id", "format", "quantity", "description_arr"],
        "release_master": ["release_id", "master_id", "is_main_release"],
    }
entity_map = {"artist": artist, "label": label, "release": release}
class Exporter:
    def __init__(self):
        self.conn = psycopg.connect(user = user, password=password,
                                    host=host, port=port, dbname=database)
        self.cur = self.conn.cursor()

    def loader(self, q, entity_type):
        entity = entity_map[entity_type]
        while q:
            curr = q.pop()
            for table_name in entity:
                cols = entity[table_name]
                #get values
                if table_name in ["releases", "labels", "artists", "release_master"]:
                    if table_name == "releases":
                        values= curr.get_release()
                    elif table_name == "labels":
                        values = curr.get_label()
                    elif table_name == "labels":
                        values = curr.get_artist()
                    else:
                        values = curr.get_release_master()
                    query = (sql.SQL("INSERT INTO {} ({}) VALUES ({})")
                         .format(sql.Identifier(table_name),
                                 sql.SQL(', ').join(map(sql.Identifier, cols)),
                                 sql.SQL(', ').join(sql.Placeholder() * len(cols))))
                    self.cur.execute(query, values)
                    self.conn.commit()
                else:
                    method_name = "get_" + table_name
                    instance_method = getattr(curr, method_name)
                    values = instance_method()
                    print(values)
                    query = (sql.SQL("INSERT INTO {} ({}) VALUES ({})")
                            .format(sql.Identifier(table_name),
                            sql.SQL(', ').join(map(sql.Identifier, cols)),
                            sql.SQL(', ').join(sql.Placeholder() * len(cols))))
                    print(query.as_string(self.conn))
                    self.cur.executemany(query, values)
                    self.conn.commit()
        self.conn.close()













