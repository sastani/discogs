import re
def cleanup_duration(id, duration):
    valid_patterns = ['\d{2}:\d{2}:\d{2}', '\d{1}:\d{2}:\d{2}', '\d{2}:\d{2}', '\d{2}:\d{1}', '\d{1}:\d{2}', '\d{1}:\d{1}']
    alternative_patterns = ['\d{2}\.\d{2}', '\d{1}\.\d{2}']
    valid_duration = False
    alt_duration = False
    duration_parts = None
    for p in valid_patterns:
        if re.match(p, duration):
            valid_duration = True
            break
    if valid_duration:
        duration_parts = duration.split(':')
    else:
        for alt in alternative_patterns:
            if re.match(alt, duration):
                alt_duration = True
                break
        if alt_duration:
            duration_parts = duration.split('.')
    return duration_parts

def convert_duration(duration_as_list):
    num_places = len(duration_as_list)
    if num_places == 1:
        seconds = int(duration_as_list[0])
        temp = seconds
        seconds = seconds % 60
        minutes = temp // 60
        hours = 0
    elif num_places == 2:
        minutes, seconds = map(int, duration_as_list)
        temp_sec = seconds
        seconds = seconds % 60
        temp_min = minutes
        minutes = (minutes % 60) + (temp_sec//60)
        hours = temp_min // 60
    elif num_places == 3:
        hours, minutes, seconds = map(int, duration_as_list)
        temp_sec = seconds
        seconds = seconds % 60
        #temp_min = minutes
        minutes = (minutes % 60) + (temp_sec//60)
        hours = hours + minutes//60
    #forget about any tracks that won't fit in (hh:mm:ss), i.e. a day long
    else:
        return None, None, None

    return hours, minutes, seconds

def get_row(fields, values, test):
    if test:
        return dict(zip(fields, values))
    else:
        return values


# if in test mode, get values with their attribute labels
def get_rows(fields, values, test):
    if test:
        return [dict(zip(fields, v)) for v in values]
    else:
        return values