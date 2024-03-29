from ..models.utils import get_row, get_rows, cleanup_duration, convert_duration
class Release:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.is_main_release = None
        self.title = None
        self.release_year = None
        self.release_month = None
        self.release_day = None
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

    #get corresponding rows for each release entity
    def get_release(self, test=False):
        fields = ["id", "title", "country", "release_year", "release_month", "release_day", "released_string", "status", "data_quality"]
        values = (self.id, self.title, self.country, self.release_year, self.release_month, self.release_day, self.release_date, self.status, self.quality)
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

    def get_release_tracks(self, log, test=False):
        fields = ["release_id", "track_title", "track_number", "position", "duration", "duration_string"]
        values = list()
        #convert track duration to correct format (with hours)
        for track in self.get_tracks():
            duration = track.get("duration")
            processed_duration = None
            if duration:
                duration_as_list = cleanup_duration(self.id, duration)
                if duration_as_list:
                    hours, minutes, seconds = convert_duration(self.id, log, duration, duration_as_list)
                    if hours is not None and minutes is not None and seconds is not None:
                        processed_duration = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
                    #print(track["duration"])
                #if it did not match any of the possible patterns, log it
                else:
                    bad_track = zip(fields, (self.id, track.get("title"), track.get("track_number"), processed_duration, duration))
            values.append((self.id, track.get("title"), track.get("track_number"), track.get("position"), processed_duration, duration))
        return get_rows(fields, values, test)

    def get_release_labels(self, test=False):
        fields = ["release_id", "label_id", "label_name", "catalog_num"]
        labels_dict = dict()
        for label in self.get_labels():
            label_id = label.get("id")
            if label_id in labels_dict:
                label_dict = labels_dict[label_id]
                cat_nums = label_dict["catno"]
                cat_nums.append(label.get("catno"))
            else:
                label_dict = dict()
                label_dict["id"] = label.get("id")
                label_dict["name"] = label.get("name")
                label_dict["catno"] = [label.get("catno")]
                labels_dict[label_id] = label_dict
        values = [(self.id, label.get("id"), label.get("name"), label.get("catno")) for label in labels_dict.values()]
        return get_rows(fields, values, test)

    def get_release_formats(self, test=False):
        fields = ["release_id", "format", "quantity_string", "free_text", "description_arr"]
        values = [(self.id, format.get("format"), format.get("quantity"), format.get("free_text"), format.get("description")) for format in self.get_formats()]
        return get_rows(fields, values, test)

    def get_release_master(self, test=False):
        fields = ["release_id", "master_id", "is_main_release"]
        values = (self.id, self.master_id, self.is_main_release)
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
        self.release_date = date
        year = month = day = None
        invalid_date = False
        nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        #validate release date string has valid characters
        for c in date:
            if c not in nums and c != '-':
                invalid_date = True
        if not invalid_date:
            date_part = date.split('-')
            date_list = list()
            for part in date_part:
                if part != '':
                    date_list.append(part)
            num_parts = len(date_list)
            if num_parts == 1:
                year = int(date_list[0])
            elif num_parts == 2:
                year = int(date_list[0])
                month = int(date_list[1])
            elif num_parts == 3:
                year = int(date_list[0])
                month = int(date_list[1])
                day = int(date_list[2])
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
        self.master_id = master

    def set_is_main_release(self, bool_val):
        self.is_main_release = bool_val


