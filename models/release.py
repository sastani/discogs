class Release:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.is_main_release = False
        self.title = None
        self.release_date = None
        self.country = None
        self.notes = None
        self.quality = None
        self.master_id = None
        self.artists = list()
        self.labels = list()
        self.formats = list()
        self.tracks = list()
        self.genres = list()
        self.styles = list()


    def set_title(self, title):
        self.title = title

    def set_release_date(self, date):
        self.release_date = date

    def set_country(self, country):
        self.country = country

    def set_notes(self, notes):
        self.notes = notes

    def set_quality(self, quality):
        self.quality = quality

    def set_master(self, master):
        self.master = master

    def set_is_main_release(self):
        self.is_main_release = True

    def get_release(self):
        fields = ["id", "status", "title", "release_date", "country"]
        values = [self.id, self.status, self.title, self.release_date, self.country]
        release = dict(zip(fields, values))
        return release

    def get_artists(self):
        return self.artists

    def get_labels(self):
        return self.labels

    def get_formats(self):
        return self.formats

    def get_genres(self):
        return self.genres

    def get_styles(self):
        return self.styles

    def get_tracks(self):
        return self.tracks

