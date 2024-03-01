from models.utils import get_row, get_rows, get_webpage_type
class Label:
    def __init__(self, id, label_name):
        self.id = id
        self.label_name = label_name
        self.sublabels = None
        self.parent_label = None
        self.contact_info = None
        self.quality = None
        self.profile = None
        self.url_strings = list()
        self.sub_labels = list()

    def set_parent_label(self, parent):
        self.parent_label = parent

    def set_contact_info(self, ci):
        self.contact_info = ci

    def set_quality(self, quality):
        self.quality = quality

    def set_profile(self, profile):
        self.profile = profile

    def get_label(self, test=False):
        fields = ["id", "label_name", "parent_label", "contact_info", "quality", "profile"]
        values = [self.id, self.label_name, self.parent_label, self.contact_info, self.quality, self.profile]
        return get_row(fields, values, test)

    def get_label_urls(self, test=False):
        fields = ["label_id", "url", "page_type"]
        label_url_row = dict()
        label_url_strings = self.get_urls()
        label_urls = list()
        for url in label_url_strings:
            label_url_row['url'] = url
            webpage_type = get_webpage_type(self.id, url)
            label_url_row['type'] = webpage_type
            label_urls.append(label_url_row)
        values = [(self.id, label.get("url"), label.get("type")) for label in label_urls]
        return get_rows(fields, values, test)

    def get_label_sublabels(self, test=False):
        fields = ["label_id", "sublabel", "sublabel_name"]
        label_sublabels = self.get_sub_labels()
        values = [(self.id, sublabel.get("id"), sublabel.get("name")) for sublabel in label_sublabels]
        return get_rows(fields, values, test)

    def get_urls(self):
        return self.url_strings

    def set_sub_labels(self, sublabels):
        self.sublabels = sublabels

    def get_sub_labels(self):
        return self.sublabels
