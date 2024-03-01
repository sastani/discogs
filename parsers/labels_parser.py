from lxml import etree
from models.label import Label
from database.loaders.export import Exporter
def parse_xml(file_name):
    #context = etree.iterparse(file_name, events=('end',))
    #advance iterator to root element
    #event, root = next(context)
    #context = etree.iterwalk(context, events=('end',))
    #advance iterator to release/child of root
    E = Exporter()
    all_labels = list()
    context = etree.iterparse(file_name, tag="label")
    for event, element in context:
        i = find_id(element)
        n = find_name(element)
        if i is not None and n is not None:
            label = Label(i, n)
            walk_context = etree.iterwalk(element, events=('end',))
            for event_label, label_element in walk_context:
                tag = label_element.tag
                text = label_element.text
                if tag == "contactinfo":
                    label.set_contact_info(text)
                elif tag == "profile":
                    label.set_profile(text)
                elif tag == "data_quality":
                    label.set_quality(text)
                elif tag == "parentLabel":
                    parent_label_id = label_element.get('id')
                    label.set_parent_label(parent_label_id, text)
                elif tag == "urls":
                    label_urls = label.get_urls()
                    for url in label_element:
                        url_path = url.text
                        if url_path:
                            label_urls.append(url_path)
                elif tag == "sublabels":
                    label_sub_labels = list()
                    for sub_label in label_element:
                        sub_label_row = sub_label.attrib
                        sub_label_name = sub_label.text
                        if sub_label_row:
                            sub_label_row['name'] = sub_label_name
                            label_sub_labels.append(sub_label_row)
                    label.set_sub_labels(label_sub_labels)
            all_labels.append(label)
    if all_labels:
        E.load_all(all_labels, "label")
    E.close_connection()

def find_id(element):
    i = element.find('id')
    if i is not None:
        return i.text

def find_name(element):
    n = element.find('name')
    if n is not None:
        return n.text
