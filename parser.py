from lxml import etree
from collections import deque

def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #event, root = next(context)
    #attributes = ["id"]
    for event, element in context:
        tag = element.tag
        #if we have found "start" of release, build release object
        if event == "start" and tag == "release":
            release = dict()
            release_tracks = dict()
            release_id = element.get('id')
            release['release_id'] = release_id
            release_status = element.get('status')
            release['status'] = release_status
            release_tracks['release_id'] = release_id
        else:
            if event == "start" and tag == "artists":
                for child in element.iterchildren():
                    add_children(release, child)
            elif event == "start" and tag == "labels":
                event, element = next(context)
                label_attributes = element.attrib
                print(label_attributes)
                #get label element
                #event, element = next(context)
                #prefix = "label"
                #add_children(release, element)
            elif event == "start" and tag == "tracklist":
                for child in element.iterchildren():
                    add_children(release_tracks, child)

    return release

def add_children(obj, element):
    #use "track", "artist", etc as prefix for key
    prefix = element.tag
    for child in element:
        key = child.tag
        val = child.text
        if val is not None:
            obj[prefix + "_" + key] = val
