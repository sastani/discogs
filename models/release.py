class ReleaseObject:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.title = ""
        self.release_date = ""
        self.country = ""
        self.artists = list()
        self.labels = list()
        self.tracks = list()
        self.genres = list()
        self.styles = list()

    def set_title(self, title):
        self.title = title

    def set_release_date(self, date):
        self.release_date = date

    def set_country(self, country):
        self.country = country

    def get_release(self):
        fields = ["id", "status", "title", "release_date", "country"]
        values = [self.id, self.status, self.title, self.release_date, self.country]
        rel = dict(zip(fields, values))
        return rel

    def get_artists(self):
        return self.artists

    def get_labels(self):
        return self.labels

    def get_genres(self):
        return self.genres

    def get_styles(self):
        return self.styles

    def get_tracks(self):
        return self.tracks
