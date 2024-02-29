from lxml import etree
from collections import deque
from models.label import Label
from parsers.utils import *

def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #advance iterator to root element
    event, root = next(context)
    context = etree.iterwalk(root, events=('start','end'))
    #advance iterator to release/child of root
    next(context)
    all_labels = deque()

    for event, element in context:
        tag = element.tag
        # if we have found "start" of label, build label object
        if event == "start" and tag == "label":
            label_id = None
            label_name = None
            for child in element.iterchildren():
                text = child.text
                child = child.tag
                if child == "images":
                    continue
                elif child == "id":
                    label_id = text
                elif child == "name":
                    label_name = text
                else:
                    break
            #create label object once id and name found
            label = Label(label_id, label_name)
            for child in element.iterchildren():
                child_element = child
                text = child.text
                child = child.tag
                if child == "contactinfo":
                    label.set_contact_info(text)
                elif child == "profile":
                    label.set_profile(text)
                elif child == "data_quality":
                    label.set_quality(text)
                elif child == "parentlabel":
                    label.set_parent_label(text)
                elif child == "urls":
                    label_urls = label.get_urls()
                    for url in child_element:
                        label_url_row = dict()
                        url_path = url.text
                        if url_path:
                            label_url_row['url'] = url_path
                            print(url_path)
                            webpage_type = get_webpage_type(label_name, url_path)
                            label_url_row['type'] = webpage_type
                            label_urls.append(label_url_row)
                elif child == "sublabels":
                    label_sub_labels = label.get_sub_labels()
                    for sub_label in child_element:
                        sub_label_row = child_element.attrib
                        #add_attributes(sub_label_row, sub_label)
                        sub_label_name = sub_label.text
                        sub_label_row['name'] = sub_label_name
                        label_sub_labels.append(sub_label_row)
        elif event == "end" and tag == "label":
            all_labels.append(label)
        context.skip_subtree()
    return all_labels

def add_children(d, element):
    for child in element:
        key = child.tag
        val = child.text
        if val is not None:
            d[key] = val

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
