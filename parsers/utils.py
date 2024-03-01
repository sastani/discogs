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