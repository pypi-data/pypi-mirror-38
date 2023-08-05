from functools import reduce as r


deepget = lambda dictionary, target:\
    r(lambda d, key: d.get(key) if d else None, target.split('.'), dictionary)
