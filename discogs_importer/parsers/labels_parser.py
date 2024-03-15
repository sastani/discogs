from lxml import etree
from ..models.label import Label
from ..database.loaders.export import Exporter
from ..parsers.utils import find_id, find_name
def parse_xml(file_name):
    E = Exporter()
    all_labels = list()
    context = etree.iterparse(file_name, tag="label")
    for event, element in context:
        label_id = find_id(element)
        name = find_name(element)
        if label_id is not None and name is not None:
            label = Label(label_id, name)
            for label_element in element:
                tag = label_element.tag
                text = label_element.text
                if tag == "images":
                    continue
                elif tag == "id":
                    continue
                elif tag == "name":
                    continue
                elif tag == "contactinfo":
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
                    for sub_label_element in label_element:
                        sub_label_row = dict()
                        sub_label_row['id'] = sub_label_element.get('id')
                        sub_label_row['name'] = sub_label_element.text
                        label_sub_labels.append(sub_label_row)
                    label.set_sub_labels(label_sub_labels)
            all_labels.append(label)
            #reset/remove element only after all children fully processed!
            element.clear()
    if all_labels:
        E.load_all(all_labels, "label")
    E.close_connection()