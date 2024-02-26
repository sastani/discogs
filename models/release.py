from models.utils import get_row, get_rows
import datetime
class Release:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.is_main_release = False
        self.title = None
        self.release_year = None
        self.release_month = None
        self.release_day = None
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

    #get corresponding rows for each release entity
    def get_release(self, test=False):
        fields = ["id", "title", "country", "release_year", "release_month", "release_day", "status", "data_quality"]
        values = (self.id, self.title, self.country, self.release_year, self.release_month, self.release_day, self.status, self.quality)
        return get_row(fields, values, test)

    def get_release_artists(self, test=False):
        fields = ["release_id", "artist_id", "artist_name", "ordinal", "join_string"]
        values = list()
        artists = self.get_artists()
        for i in range(0, len(artists)):
            artist = artists[i]
            ordinal = i + 1
            values.append((self.id, artist.get("id"), artist.get("name"), ordinal, artist.get("join")))
        return get_rows(fields, values, test)


    def get_release_genres(self, test=False):
        fields = ["release_id", "genre"]
        values = [(self.id, genre) for genre in self.get_genres()]
        return get_rows(fields, values, test)

    def get_release_styles(self, test=False):
        fields = ["release_id", "style"]
        values = [(self.id, style) for style in self.get_styles()]
        return get_rows(fields, values, test)

    def get_release_tracks(self, test=False):
        fields = ["release_id", "track_title", "track_number", "position", "duration"]
        values = list()
        #convert track duration to correct format (with hours)
        for track in self.get_tracks():
            duration = track.get("duration")
            if duration:
                duration_parts = duration.split(':')
                if len(duration_parts) == 2:
                    hours = 0
                    minutes, seconds = map(int, duration_parts)
                else:
                    hours, minutes, seconds = map(int, duration_parts)
                track["duration"] = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
            values.append((self.id, track.get("title"), track.get("track_number"), track.get("position"), track.get("duration")))
        return get_rows(fields, values, test)

    def get_release_labels(self, test=False):
        fields = ["release_id", "label_id", "label_name", "catalog_num"]
        values = [(self.id, label.get("id"), label.get("name"), label.get("catno")) for label in self.get_labels()]
        return get_rows(fields, values, test)

    def get_release_formats(self, test=False):
        fields = ["release_id", "format", "quantity", "description_arr"]
        values = [(self.id, format.get("format"), format.get("quantity"), format.get("description")) for format in self.get_formats()]
        return get_rows(fields, values, test)

    def get_release_master(self, test=False):
        fields = ["release_id", "master_id", "is_main_release"]
        values = (self.id, self.master, self.is_main_release)
        return get_row(fields, values, test)


    #getters and setters
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

    def set_title(self, title):
        self.title = title

    def set_release_date(self, date):
        date_part = date.split('-')
        num_parts = len(date_part)
        year = month = day = None
        if num_parts == 1:
            year = int(date_part[0])
        if num_parts == 2:
            year = int(date_part[0])
            month = int(date_part[1])
        elif num_parts == 3:
            year = int(date_part[0])
            month = int(date_part[1])
            day = int(date_part[2])
        self.release_year = year
        self.release_month = month
        self.release_day = day

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

