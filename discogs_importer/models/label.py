from ..models.utils import get_row, get_rows, get_webpage_type
class Label:
    def __init__(self, id, label_name):
        self.id = id
        self.label_name = label_name
        self.sublabels = None
        self.parent_label_id = None
        self.parent_label = None
        self.contact_info = None
        self.quality = None
        self.profile = None
        self.url_strings = list()
        self.sub_labels = list()

    def set_parent_label(self, id, parent):
        self.parent_label_id = id
        self.parent_label = parent

    def set_contact_info(self, ci):
        self.contact_info = ci

    def set_quality(self, quality):
        self.quality = quality

    def set_profile(self, profile):
        self.profile = profile

    def get_label(self, test=False):
        fields = ["id", "label_name", "parent_label_id", "parent_label", "contact_info", "profile", "data_quality"]
        values = [self.id, self.label_name, self.parent_label_id, self.parent_label, self.contact_info, self.profile, self.quality]
        return get_row(fields, values, test)

    def get_label_urls(self, log, test=False):
        fields = ["label_id", "url", "page_type"]
        label_url_strings = self.get_urls()
        label_urls = list()
        seen_urls = set()
        for url in label_url_strings:
            #dont add duplicate urls
            if url not in seen_urls:
                label_url_row = dict()
                label_url_row['url'] = url
                webpage_type = get_webpage_type(self.id, log, self.label_name.lower(), url.lower(), "label")
                label_url_row['type'] = webpage_type
                label_urls.append(label_url_row)
                seen_urls.add(url)
        #values = list()
        values = [(self.id, label_url.get("url"), label_url.get("type")) for label_url in label_urls if label_url]
        return get_rows(fields, values, test)

    def get_label_sublabels(self, test=False):
        fields = ["label_id", "sublabel", "sublabel_name"]
        label_sublabels = self.get_sub_labels()
        print(self.id)
        print(label_sublabels)
        if label_sublabels:
            values = [(self.id, sublabel.get("id"), sublabel.get("name")) for sublabel in label_sublabels]
            return get_rows(fields, values, test)
        #if label does not have any sublabels
        else:
            return None

    def get_urls(self):
        return self.url_strings

    def set_sub_labels(self, sublabels):
        self.sublabels = sublabels

    def get_sub_labels(self):
        return self.sublabels
