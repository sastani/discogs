from lxml import etree
from collections import deque
from models.release import ReleaseObject

def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #advance iterator to root element
    event, root = next(context)
    context = etree.iterwalk(root, events=('start','end'))
    #advance iterator to release/child of root
    next(context)
    all_releases = deque()

    for event, element in context:
        tag = element.tag
        text = element.text
        # if we have found "start" of release, build release object
        if event == "start" and tag == "release":
            release_id = element.get('id')
            release_status = element.get('status')
            release = ReleaseObject(release_id, release_status)
        # if we have found "end" of release, add release object to queue
        elif event == "end" and tag == "release":
            all_releases.append(release)
        else:
            if event == "start" and tag == "artists":
                for artist in element.iterchildren():
                    artist_row = dict()
                    add_children(artist_row, artist)
                    release.get_artists().append(artist_row)
                    # print(release.get_artists())
            elif event == "start" and tag == "title":
                release.set_title(element.text)
                # print(release.get_title())
            elif event == "start" and tag == "labels":
                for label in element.iterchildren():
                    label_row = dict()
                    add_attributes(label_row, label)
                    release.get_labels().append(label_row)
                    # print(release.get_labels())
            elif event == "start" and tag == "formats":
                for format in element.iterchildren():
                    format_row = dict()
                    format_description = list()
                    for descriptions in format:
                        for description in descriptions:
                            format_description.append(description.text)
                    format_row['release_id'] = release_id
                    format_row['description'] = format_description
                    release.get_formats().append(format_row)
            elif event == "start" and tag == "genres":
                for genre in element.iterchildren():
                    genre_row = dict()
                    genre_row['release_id'] = release_id
                    key = genre.tag
                    val = genre.text
                    if val is not None:
                        genre_row[key] = val
                    release.get_genres().append(genre_row)
            elif event == "start" and tag =="styles":
                for style in element.iterchildren():
                    style_row = dict()
                    style_row['release_id'] = release_id
                    key = style.tag
                    val = style.text
                    if val is not None:
                        style_row[key] = val
                    release.get_styles().append(style_row)
            elif event == "start" and tag == "country":
                release.set_country(text)
            elif event == "start" and tag == "released":
                release.set_release_date(text)
            elif event == "start" and tag == "tracklist":
                for track in element.iterchildren():
                    track_row = dict()
                    track_row['release_id'] = release_id
                    add_children(track_row, track)
                    release.get_tracks().append(track_row)
            #skip parsing any children/descendants of release
            context.skip_subtree()
    return all_releases

def add_children(d, element):
    #use "track", "artist", etc as prefix for key
    prefix = element.tag
    for child in element:
        key = child.tag
        val = child.text
        if val is not None:
            d[prefix + "_" + key] = val

def add_children_only(d, element):
    key = element.tag
    val = element.text
    if val is not None:
        d[key] = val


def add_attributes(d, element):
    prefix = element.tag
    attributes = element.attrib
    for a in attributes:
        val = attributes[a]
        d[prefix + "_" + a] = val
