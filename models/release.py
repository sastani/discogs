class ReleaseObject:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.artists = list()
        self.labels = list()
        self.tracks = list()

    def get_artists(self):
        return self.artists

    def get_labels(self):
        return self.labels

    def get_tracks(self):
        return self.tracks
