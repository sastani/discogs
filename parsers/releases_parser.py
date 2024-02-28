from lxml import etree
from models.release import Release
from parsers.utils import *
from database.loaders.export import Exporter

def parse_xml(file_name, chunk_size):
    context = etree.iterparse(file_name, events=("end",), tag="release")
    #context = iter(context)
    #advance iterator to root element
    #event, root = next(context)
    #context = etree.iterwalk(root, events=('start', 'end'))
    #event, root = next(context)


    all_releases = list()
    E = Exporter()
    file = open('output.log', 'a')
    for event, release_element in context:
        release_id = release_element.get('id')
        release_status = release_element.get('status')
        release = Release(release_id, release_status)
        elem_as_string = etree.tostring(release_element)
        #print("----------")
        #print(elem_as_string)
        if event == "end":
            for child in release_element.iterchildren():
                elem_as_string_2 = etree.tostring(child)
                tag = child.tag
                text = child.text
                #print(elem_as_string_2)
                #file.write("this is release: " + release_id + "\n")
                #file.write("this is the element: " + str(elem_as_string) + "\n")
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
                        label_row = label.attrib
                        release.get_labels().append(label_row)
                elif tag == "extraartists":
                    continue
                elif tag == "formats":
                    for format in child.iterchildren():
                        format_row = dict()
                        format_description = list()
                        format_row['format'] = format.get('name')
                        format_row['quantity'] = format.get('qty')
                        format_row['free_text'] = format.get('text')
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
                    if text:
                        release.set_release_date(text)
                elif tag == "notes":
                    release.set_notes(text)
                elif tag == "data_quality":
                    release.set_quality(text)
                elif tag =="master_id":
                    release.set_master(text)
                    main_release = child.get('is_main_release')
                    if main_release:
                        release.set_is_main_release()
                elif tag == "tracklist":
                    track_counter = 1
                    for track in child.iterchildren():
                        track_row = dict()
                        add_children(track_row, track)
                        track_row["track_number"] = track_counter
                        track_counter += 1
                        release.get_tracks().append(track_row)
        all_releases.append(release)
        release_element.clear()
        if len(all_releases) == chunk_size:
            E.loader(all_releases, "release")
            all_releases = list()

    if all_releases:
        E.loader(all_releases, "release")

    E.close_connection()

        #context.skip_subtree()
        #next(context)
        #root.clear()
        # if we have found "end" of release, add release object to queue
    #if all_releases:
        #E.loader(all_releases, "release")

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
