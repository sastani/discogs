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