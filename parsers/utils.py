def extract_webpage(url):
    if '/' in url:
        url_parts = url.split('/')
        domain = url_parts[2]
    else:
        domain = url
    domain_parts = domain.split('.')
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
    webpage_type = extract_webpage(url_path)
    name_list = convert_name_to_list(name)
    for n in name_list:
        if n in webpage_type:
            webpage_type = "website"
            return webpage_type
    return webpage_type

def add_children(d, element):
    for child in element:
        key = child.tag
        val = child.text
        if val is not None:
            d[key] = val

def add_children_only(d, element):
    key = element.tag
    val = element.text
    if val is not None:
        d[key] = val