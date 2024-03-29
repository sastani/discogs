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
log = open('output.log', 'a')

#table name and column/attributes for each table
artist = \
    {
        "artist": ["id", "artist_name", "name", "profile", "data_quality"],
        "artist_name_variations": ["artist_id", "name"],
        "artist_aliases": ["artist_id", "alias_artist_id", "alias_name"],
        "artist_groups": ["artist_id", "group_artist_id", "group_name"],
        "artist_urls": ["artist_id", "url", "page_type"]
    }
label = \
    {
        "label": ["id", "name", "parent_label_id", "parent_label_name", "contact_info", "profile",
                   "data_quality"],
        "label_sublabels": ["label_id", "sublabel_label_id", "sublabel_label_name"],
        "label_urls": ["label_id", "url", "page_type"]
    }
release =\
    {
        "release": ["id", "title", "country", "release_year", "release_month", "release_day", "released_string", "status", "data_quality"],
        "release_artists": ["release_id", "artist_id", "artist_name", "ordinal", "join_string"],
        "release_genres": ["release_id", "genre"],
        "release_styles": ["release_id", "style"],
        "release_tracks": ["release_id", "track_title", "track_number", "position", "duration", "duration_string"],
        "release_labels": ["release_id", "label_id", "label_name", "catalog_nums"],
        "release_formats": ["release_id", "format", "quantity_string", "text", "description_arr"],
        "release_master": ["release_id", "master_id", "is_main_release"],
    }
entity_map = {"artist": artist, "label": label, "release": release}
class Exporter:
    def __init__(self):
        self.conn = psycopg.connect(user = user, password=password,
                                    host=host, port=port, dbname=database)
        self.cur = self.conn.cursor()

    def load_all(self, q, entity_type):
        entity = entity_map[entity_type]
        for table_name in entity:
            self.load_table(q, entity, table_name)

    def load_table(self, q, entity, table_name):
        table_values = list()
        cols = entity[table_name]
        flatten = False
        if table_name not in ["release", "label", "artist", "release_master"]:
            flatten = True
        query, table_values = self.create_query(q, table_name, cols, table_values)
        self.execute_query(query, table_values, flatten)

    def create_query(self, q, table_name, cols, table_values):
        for curr in q:
            method_name = "get_" + table_name
            #get values
            if method_name == "get_release_tracks":
                values = curr.get_release_tracks(log, False)
            elif method_name == "get_label_urls":
                values = curr.get_label_urls(log, False)
            elif method_name == "get_artist_urls":
                values = curr.get_artist_urls(log, False)
            else:
                instance_method = getattr(curr, method_name)
                values = instance_method()
            if values:
                table_values.append(values)
        query = (sql.SQL("INSERT INTO {} ({}) VALUES ({})")
                 .format(sql.Identifier(table_name),
                         sql.SQL(', ').join(map(sql.Identifier, cols)),
                         sql.SQL(', ').join(sql.Placeholder() * len(cols))))
        return query, table_values

    def execute_query(self, query, table_values, flatten):
        if flatten:
            table_values = flatten_list(table_values)
        self.cur.executemany(query, table_values)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
        log.close()


def flatten_list(list_of_lists):
    flattened = list()
    for l in list_of_lists:
        for t in l:
            flattened.append(t)
    return flattened
