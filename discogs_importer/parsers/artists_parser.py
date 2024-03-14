from lxml import etree
from ..models.artist import Artist
from ..database.loaders.export import Exporter
from ..parsers.utils import find_id, find_name

def parse_xml(file_name, chunk_size):
    E = Exporter()
    all_artists = list()
    context = etree.iterparse(file_name, tag="artist")

    for event, element in context:
        artist_id = find_id(element)
        name = find_name(element)
        if artist_id is not None and name is not None:
            artist = Artist(artist_id, name)
            for artist_element in element:
                tag = artist_element.tag
                text = artist_element.text
                if tag == "images":
                    continue
                elif tag == "id":
                    continue
                elif tag == "name":
                    continue
                elif tag == "realname":
                    artist.set_name(text)
                elif tag  == "profile":
                    artist.set_profile(text)
                elif tag == "data_quality":
                    artist.set_quality(text)
                elif tag == "urls":
                    artist_urls = artist.get_urls()
                    for url_element in artist_element:
                        url_path = url_element.text
                        print(url_path)
                        if url_path:
                            artist_urls.append(url_path)
                elif tag == "namevariations":
                    name_variations = artist.get_name_variations()
                    for name_variation_element in artist_element:
                        name_variation = name_variation_element.text
                        name_variations.append(name_variation)
                elif tag == "aliases":
                    aliases = artist.get_aliases()
                    for alias_element in artist_element:
                        artist_aliases_row = dict()
                        artist_aliases_row['id'] = alias_element.get('id')
                        artist_aliases_row['alias'] = alias_element.text
                        aliases.append(artist_aliases_row)
                elif tag == "groups":
                    groups = artist.get_groups()
                    for group_element in artist_element:
                        artist_groups_row = dict()
                        artist_groups_row['id'] = group_element.get('id')
                        artist_groups_row['group'] = group_element.text
                        groups.append(artist_groups_row)
            all_artists.append(artist)
        element.clear()
        if len(all_artists) == chunk_size:
            E.load_all(all_artists, "artist")
            all_artists = list()
    if all_artists:
        E.load_all(all_artists, "artist")
    E.close_connection()