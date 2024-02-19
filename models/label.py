class Label:
    def __init__(self, id, label_name):
        self.id = id
        self.label_name = label_name
        self.parent_label = None
        self.contact_info = None
        self.quality = None
        self.profile = None

        self.urls = list()
        self.sub_labels = list()

    def set_parent_label(self, parent):
        self.parent_label = parent

    def set_contact_info(self, ci):
        self.contact_info = ci

    def set_quality(self, quality):
        self.quality = quality

    def set_profile(self, profile):
        self.profile = profile

    def get_label(self):
        fields = ["id", "label_name", "parent_label", "contact_info", "quality", "profile",]
        values = [self.id, self.label_name, self.parent_label, self.contact_info, self.quality, self.profile]
        label = dict(zip(fields, values))
        return label

    def get_urls(self):
        return self.urls

    def get_sub_labels(self):
        return self.sub_labels
