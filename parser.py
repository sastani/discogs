from lxml import etree
from collections import deque

class ReleaseObject():
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.artist_id = None
        self.artist_name = None
        self.labels = list()
        self.tracks = list()

    def set_artist(self, name, id):
        self.artist_name = name
        self.artist_id = id

    def get_labels(self):
        return self.labels

    def get_tracks(self):
        return self.tracks


def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #event, root = next(context)
    #attributes = ["id"]
    for event, element in context:
        tag = element.tag
        #if we have found "start" of release, build release object
        if event == "start" and tag == "release":
            release = dict()
            release_tracks = list()
            release_labels = list()
            release_id = element.get('id')
            release_status = element.get('status')
            #release = ReleaseObject(release_id, release_status)
        else:
            if event == "start" and tag == "artists":
                for artist in element.iterchildren():
                    add_children(release, artist)
            elif event == "start" and tag == "labels":
                for label in element.iterchildren():
                    label_row = dict()
                    add_attributes(label_row, label)
                    print(label_row)
                #get label element
                #event, element = next(context)
                #prefix = "label"
                #add_children(release, element)
            elif event == "start" and tag == "tracklist":
                for track in element.iterchildren():
                    track_row = dict()
                    add_children(track_row, track)
                    track_row['release_id'] = release_id
                    print(track_row)
                    release_tracks.append(track_row)

    return release

def add_children(d, element):
    #use "track", "artist", etc as prefix for key
    prefix = element.tag
    for child in element:
        key = child.tag
        val = child.text
        if val is not None:
            d[prefix + "_" + key] = val
    print(d)

def add_attributes(d, element):
    prefix = element.tag
    attributes = element.attrib
    for a in attributes:
        val = attributes[a]
        d[prefix + "_" + a] = val

parse_xml('/Volumes/WD Black/Discogs/sample_release/release-3068908.xml')