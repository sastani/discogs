from lxml import etree
from collections import deque
from models.artist import ArtistObject

def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #advance iterator to root element
    event, root = next(context)
    context = etree.iterwalk(root, events=('start','end'))
    #advance iterator to release/child of root
    next(context)
    all_artists = deque()

    for event, element in context:
        tag = element.tag
        text = element.text
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
            artist = ArtistObject(artist_id, artist_name)
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
                    artist_url_row = dict()
                    for url in child_element.iterchildren():
                        url_path = url.text
                        artist_url_row['url'] = url_path
                        artist_urls.append(artist_url_row)
        # if we have found "end" of release, add release object to queue
        elif event == "end" and tag == "artist":
            all_artists.append(artist)
    return all_artists
