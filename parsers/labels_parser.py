from lxml import etree
from models.label import Label
from database.loaders.export import Exporter

def parse_xml(file_name):
    context = etree.iterparse(file_name, events=('start', 'end'))
    #advance iterator to root element
    event, root = next(context)
    context = etree.iterwalk(root, events=('start','end'))
    #advance iterator to release/child of root
    next(context)
    E = Exporter()
    all_labels = list()

    for event, element in context:
        tag = element.tag
        label = None
        # if we have found "start" of label, build label object
        if event == "start" and tag == "label":
            label_id = None
            label_name = None
            for child in element.iterchildren():
                text = child.text
                tag = child.tag
                if tag == "images":
                    continue
                elif tag == "id":
                    label_id = text
                elif tag == "name":
                    label_name = text
                else:
                    break
            if label_id and label_name:
                #create label object once id and name found
                label = Label(label_id, label_name)
            for child in element.iterchildren():
                text = child.text
                tag = child.tag
                if tag == "contactinfo":
                    label.set_contact_info(text)
                elif tag == "profile":
                    label.set_profile(text)
                elif tag == "data_quality":
                    label.set_quality(text)
                elif tag == "parentlabel":
                    parent_label_id = child.get('id')
                    label.set_parent_label(parent_label_id, text)
                elif tag == "urls":
                    label_urls = label.get_urls()
                    for url in child:
                        url_path = url.text
                        if url_path:
                            label_urls.append(url_path)
                elif tag == "sublabels":
                    label_sub_labels = list()
                    for sub_label in child:
                        sub_label_row = sub_label.attrib
                        sub_label_name = sub_label.text
                        sub_label_row['name'] = sub_label_name
                        label_sub_labels.append(sub_label_row)
                    label.set_sub_labels(label_sub_labels)
        if label:
            all_labels.append(label)
        context.skip_subtree()
    if all_labels:
        E.load_all(all_labels, "label")
        context.skip_subtree()