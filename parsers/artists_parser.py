from lxml import etree
from collections import deque
from models.artist import Artist
from parsers.utils import *

def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #advance iterator to root element
    event, root = next(context)
    context = etree.iterwalk(root, events=('start','end'))
    #advance iterator to release/child of root
    event, element = next(context)
    all_artists = deque()

    for event, element in context:
        tag = element.tag
        # if we have found "start" of artist, start getting data to build artist object
        if event == "start" and tag == "artist":
            artist_id = None
            artist_name = None
            for child in element.iterchildren():
                text = child.text
                child = child.tag
                if child == "images":
                    continue
                elif child == "id":
                    artist_id = text
                elif child == "name":
                    artist_name = text
                else:
                    break
            #create artist object once id and name found
            artist = Artist(artist_id, artist_name)
            for child in element.iterchildren():
                child_element = child
                text = child.text
                child = child.tag
                if child == "realname":
                    artist.set_name(text)
                elif child == "profile":
                    artist.set_profile(text)
                elif child == "data_quality":
                    artist.set_quality(text)
                elif child == "urls":
                    artist_urls = artist.get_urls()
                    for url in child_element.iterchildren():
                        artist_url_row = dict()
                        url_path = url.text
                        print(url_path)
                        if url_path:
                            artist_url_row['url'] = url_path
                            webpage_type = get_webpage_type(artist_name, url_path)
                            artist_url_row['type'] = webpage_type
                            artist_urls.append(artist_url_row)
                elif child == "namevariations":
                    name_variations = artist.get_name_variations()
                    for name in child_element.iterchildren():
                        name_variations.append(name.text)
                elif child == "aliases":
                    aliases = artist.get_aliases()
                    for alias in child_element.iterchildren():
                        artist_aliases_row = dict()
                        artist_aliases_row['id'] = alias.get('id')
                        artist_aliases_row['alias'] = alias.text
                        aliases.append(artist_aliases_row)
                elif child == "groups":
                    groups = artist.get_groups()
                    for group in child_element.iterchildren():
                        artist_groups_row = dict()
                        artist_groups_row['id'] = group.get('id')
                        artist_groups_row['group'] = group.text
                        groups.append(artist_groups_row)
        # if we have found "end" of release, add release object to queue
        elif event == "end" and tag == "artist":
            all_artists.append(artist)
            context.skip_subtree()
        print(tag)
        print(artist_id)
        element.clear()
        #context.skip_subtree()
    return all_artists