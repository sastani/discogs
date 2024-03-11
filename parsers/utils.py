def add_children(d, element):
    for child in element:
        key = child.tag
        val = child.text
        if val is not None:
            d[key] = val

def find_id(element):
    i = element.find('id')
    if i is not None:
        return i.text

def find_name(element):
    n = element.find('name')
    if n is not None:
        return n.text
