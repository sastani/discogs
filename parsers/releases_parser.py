from lxml import etree
from collections import deque
from models.release import Release
from parsers.utils import *

def pop_last(all_releases):
    if len(all_releases) != 0:
        r = all_releases.pop()
        print("release:", r.get_release(), sep=' ')
        print("artists: ", r.get_artists(), sep=' ')
        print("labels: ", r.get_labels(), sep=' ')
        print("tracklist: ", r.get_tracks(), sep=' ')
        print("genres: ", r.get_genres(), sep=' ')
        print("styles: ", r.get_styles(), sep=' ')
        print("formats: ", r.get_formats(), sep=' ')
def parse_xml(file_name, chunk_size):
    context = etree.iterparse(file_name, events=('start', 'end'))
    context = iter(context)
    #advance iterator to root element
    event, root = next(context)

    all_releases = deque()
    counter = 0

    for event, element in context:
        release_tag = element.tag
        if counter == chunk_size:
            empty_queue(all_releases)
            counter = 0
        if event == "start" and release_tag == "release":
            release_element = element
            release_id = element.get('id')
            release_status = element.get('status')
            release = Release(release_id, release_status)
            print("release: " + str(counter))
            #pop_last(all_releases)
            for child in release_element.iterchildren():
                text = child.text
                tag = child.tag
                if tag == "images":
                    continue
                elif tag == "artists":
                    for artist in child.iterchildren():
                        artist_row = dict()
                        add_children(artist_row, artist)
                        release.get_artists().append(artist_row)
                        # print(release.get_artists())
                elif tag == "title":
                    release.set_title(text)
                    # print(release.get_title())
                elif tag == "labels":
                    for label in child.iterchildren():
                        label_row = dict()
                        add_attributes(label_row, label)
                        release.get_labels().append(label_row)
                        # print(release.get_labels())
                elif tag == "extraartists":
                    continue
                elif tag == "formats":
                    for format in child.iterchildren():
                        format_row = dict()
                        format_description = list()
                        format_row['format'] = format.get('name')
                        format_row['quantity'] = format.get('qty')
                        for descriptions in format:
                            for description in descriptions:
                                format_description.append(description.text)
                        format_row['description'] = format_description
                        release.get_formats().append(format_row)
                elif tag == "genres":
                    for genre in child.iterchildren():
                        genre_val = genre.text
                        release.get_genres().append(genre_val)
                elif tag == "styles":
                    for style in child.iterchildren():
                        style_val = style.text
                        release.get_styles().append(style_val)
                elif tag == "country":
                    release.set_country(text)
                elif tag == "released":
                    release.set_release_date(text)
                elif tag == "notes":
                    release.set_notes(text)
                elif tag == "data_quality":
                    release.set_quality(text)
                elif tag == "tracklist":
                    for track in child.iterchildren():
                        track_row = dict()
                        add_children(track_row, track)
                        release.get_tracks().append(track_row)
        # if we have found "end" of release, add release object to queue
        if event == "end" and release_tag == "release":
            all_releases.append(release)
            counter += 1
            root.clear()
        #empty any remaining objects in queue
        if not all_releases:
            empty_queue(all_releases)

       #context.skip_subtree()

        #element.clear()
        #skip parsing any children/descendants of release
        #context.skip_subtree()
    #return all_releases

def empty_queue(releases):
    while releases:
        print("-----------------")
        r = releases.pop()
        print("release:", r.get_release(), sep=' ')
        print("artists: ", r.get_artists(), sep=' ')
        print("labels: ", r.get_labels(), sep=' ')
        print("tracklist: ", r.get_tracks(), sep=' ')
        print("genres: ", r.get_genres(), sep=' ')
        print("styles: ", r.get_styles(), sep=' ')
        print("formats: ", r.get_formats(), sep=' ')
