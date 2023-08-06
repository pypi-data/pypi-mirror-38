
def replace_all(s, replacements={}):
    keys = list(replacements.keys())
    keys.sort(key=len, reverse=True)
    for key in keys:
        value = replacements[key]
        s = s.replace(key, value)
    return s