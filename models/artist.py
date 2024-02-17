class ArtistObject:
    def __init__(self, id, artist_name):
        self.id = id
        self.artist_name = artist_name
        self.name = ""
        self.quality = ""
        self.profile = ""

        self.urls = list()
        self.name_variations = list()
        self.aliases = list()
        self.groups = list()


    def set_name(self, name):
        self.name = name

    def set_quality(self, quality):
        self.quality = quality

    def set_profile(self, profile):
        self.profile = profile

    def get_artist(self):
        fields = ["id", "artist_name", "name", "quality", "profile", "name_variations"]
        values = [self.id, self.artist_name, self.name, self.quality, self.profile, self.name_variations]
        artist = dict(zip(fields, values))
        return artist

    def get_urls(self):
        return self.urls

    def get_name_variations(self):
        return self.name_variations

    def get_aliases(self):
        return self.aliases

    def get_groups(self):
        return self.groups
