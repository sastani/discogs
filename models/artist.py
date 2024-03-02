from models.utils import get_row, get_rows, get_webpage_type
class Artist:
    def __init__(self, id, artist_name):
        self.id = id
        self.artist_name = artist_name
        self.name = None
        self.quality = None
        self.profile = None
        self.url_strings = list()
        self.name_variations = list()
        self.aliases = list()
        self.groups = list()


    def set_name(self, name):
        self.name = name

    def set_quality(self, quality):
        self.quality = quality

    def set_profile(self, profile):
        self.profile = profile

    def get_artist(self, test=False):
        fields = ["id", "artist_name", "name", "quality", "profile"]
        values = [self.id, self.artist_name, self.name, self.quality, self.profile]
        return get_row(fields, values, test)

    def get_artist_name_variations(self, test=False):
        fields = ["artist_id", "name"]
        values = [(self.id, name_variation) for name_variation in self.get_name_variations()]
        return get_rows(fields, values, test)

    def get_artist_aliases(self, test=False):
        fields = ["artist_id", "alias_artist_id", "alias_name"]
        values = [(self.id, alias.get("id"), alias.get("alias")) for alias in self.get_aliases()]
        return get_rows(fields, values, test)

    def get_artist_groups(self, test=False):
        fields = ["artist_id", "group_artist_id", "group_name"]
        values = [(self.id, group.get("id"), group.get("group")) for group in self.get_groups()]
        return get_rows(fields, values, test)


    def get_artist_urls(self, log, test=False):
        fields = ["artist_id", "url", "page_type"]
        artist_url_strings = self.get_urls()
        artist_urls = list()
        seen_urls = set()
        for url in artist_url_strings:
            # dont add duplicate urls
            if url not in seen_urls:
                artist_url_row = dict()
                artist_url_row['url'] = url
                webpage_type = get_webpage_type(self.id, log, self.artist_name.lower(), url.lower(), "artist")
                artist_url_row['type'] = webpage_type
                artist_urls.append(artist_url_row)
                seen_urls.add(url)
        # values = list()
        values = [(self.id, artist_url.get("url"), artist_url.get("type")) for artist_url in artist_urls if artist_url]
        return get_rows(fields, values, test)

    def get_urls(self):
        return self.url_strings

    def get_name_variations(self):
        return self.name_variations

    def get_aliases(self):
        return self.aliases

    def get_groups(self):
        return self.groups
