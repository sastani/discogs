import re
def cleanup_duration(id, duration):
    valid_patterns = ['^\d{2}:\d{2}:\d{2}$', '^\d{1}:\d{2}:\d{2}$', '^\d{2}:\d{2}$', '^\d{2}:\d{1}$', '^\d{1}:\d{2}$', '^\d{1}:\d{1}$']
    alternative_patterns = ['^\d{2}\.\d{2}$', '^\d{1}\.\d{2}$']
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

def convert_duration(id, log, duration, duration_as_list):
    num_places = len(duration_as_list)
    try:
        if num_places == 1:
            seconds = int(duration_as_list[0])
            minutes = 0
            hours = 0
        elif num_places == 2:
            minutes, seconds = map(int, duration_as_list)
            hours = 0
        elif num_places == 3:
            hours, minutes, seconds = map(int, duration_as_list)
        else:
            return None, None, None
        mins_to_add = seconds // 60
        seconds = seconds % 60
        hours_to_add = (minutes + mins_to_add) // 60
        minutes = (minutes + mins_to_add) % 60
        hours = hours + hours_to_add
        if hours >= 24:
            return None, None, None
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("convert_duration() FAILED for release: " + id + " with duration str: " + duration + " duration list: ", duration_as_list)
        log.write("convert_duration() FAILED for release: " + id + " with duration str: \"" + duration + "\"")
        return None, None, None
    return hours, minutes, seconds

def extract_webpage(url):
    if '/' in url:
        url_parts = url.split('/')
        domain = url_parts[2]
    else:
        domain = url
    print(domain)
    domain_parts = domain.split('.')
    print(domain_parts)
    if len(domain_parts)  == 2:
        page_type = domain_parts[0]
    else:
        page_type = domain_parts[1]
    return page_type

def cleanup_name(name):
    punc = [':', ';', ',', '!', '"', '\'']
    new_name = [c.lower() for c in name if c not in punc]
    return ''.join(new_name)

def convert_name_to_list(name):
    name_list = name.split(' ')
    name_list = [cleanup_name(n) for n in name_list]
    return name_list

def get_webpage_type(name, url_path):
    is_valid = validate_url(url_path)
    if is_valid:
        webpage_type = extract_webpage(url_path)
        name_list = convert_name_to_list(name)
        for n in name_list:
            if n in webpage_type:
                webpage_type = "website"
                return webpage_type
    else:
        return None
    return webpage_type

def validate_url(url):
    patterns = ['.+\.{1}.+', '.+\.{1}.+\.{1}.+']
    for p in patterns:
        if re.match(p, url):
            return True
    return False

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