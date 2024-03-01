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

def extract_webpage(id, log, url):
    if '/' in url:
        url_parts = url.split('/')
        pattern = '.+//.+'
        pattern_two = '.+/.+/.+'
        '.+/.+/.+'
        num_parts = len(url_parts)
        if re.match(pattern, url):
            if num_parts > 2:
                domain = url_parts[2]
            else:
                domain = url_parts[0]
        else:
            domain = url_parts[0]
    else:
        domain = url
    if domain == 'linktr.ee':
        return domain
    domain_parts = domain.split('.')
    try:
        if len(domain_parts)  == 2:
            page_type = domain_parts[0]
        else:
            page_type = domain_parts[1]
    except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            error_message = "extract_webpage() FAILED for label id: " + id + " with url: " + url + "\n"
            print(error_message)
            log.write(error_message)
            return None
    return page_type

def cleanup_name(name):
    punc = [' ', ':', ';', ',', '!', '"', '\'']
    new_name = [c.lower() for c in name if c not in punc]
    return ''.join(new_name)

def convert_name_to_list(name):
    name_list = name.split(' ')
    name_list = [cleanup_name(n) for n in name_list if len(n) > 1]
    return name_list

def get_webpage_type(id, log, name, url_path):
    is_valid = validate_url(url_path)
    domain = extract_webpage(id, log, url_path)
    page_type = "other"
    if is_valid and domain is not None:
        social_pages = ['facebook', 'instagram', 'twitter', 'pinterest', 'tiktok', 'spotify', 'beatport', 'soundcloud',
                        'bandcamp','google', 'youtube', 'myspace', 'wikipedia', 'reddit', 'tumblr', 'vimeo',
                         'youtube', 'flickr', 'linktr.ee', 'discogs', 'last', 'reverbnation', 'mixcloud', 'imdb',
                        'ra', 'residentadvisor']
        if domain in social_pages:
            page_type = domain
        else:
            name_list = convert_name_to_list(name)
            name = name.replace(' ', '')
            if name in domain:
                page_type = "website"
            else:
                #check components of name (i.e. 'Siesta Music', find 'siesta' in 'siestarecordings.com'
                for n in name_list:
                    if n in domain:
                        page_type = "website"
        return page_type
    else:
        return None


def validate_url(url):
    pattern = re.compile(
        r"(\w+://)?"  # protocol                      (optional)
        r"(\w+\.)?"  # host                          (optional)
        r"(([\w-]+)\.(\w+))"  # domain
        r"(\.\w+)*"  # top-level domain              (optional, can have > 1)
        r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc.   (optional)
    )
    inner_pattern_subdomain = '(.+/)?\w{2,3}\.\w+\.\w{2,3}(/.+)?'
    inner_pattern_no_subdomain = '(.+/)?\w+.\w{2,3}(/.+)?'
    match = pattern.match(url)
    if match:
        sub_match = re.match(inner_pattern_subdomain, url)
        no_sub_match =  re.match(inner_pattern_no_subdomain, url)
        if sub_match or no_sub_match:
            return True
        else:
            return False
    else:
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