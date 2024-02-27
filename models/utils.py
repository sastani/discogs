import re
def cleanup_duration(duration):
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