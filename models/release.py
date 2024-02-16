class ReleaseObject:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.title = ""
        self.artists = list()
        self.labels = list()
        self.tracks = list()

    def set_title(self, title):
        self.title = title

    def get_release(self):
        return ("id:" + self.id + " status:" + self.status + " title:" + self.title)

    def get_artists(self):
        return self.artists

    def get_labels(self):
        return self.labels

    def get_tracks(self):
        return self.tracks
