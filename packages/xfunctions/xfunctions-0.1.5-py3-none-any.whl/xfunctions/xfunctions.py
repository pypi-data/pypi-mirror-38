# coding:utf-8


def sleep(t: int):
    import time
    import xprint as xp
    xp.wr(xp.Fore.LIGHTBLUE_EX +
          ' - [' + '-' * t + '] sleep 0/%s s' % t + '\r')
    xp.fi()

    for i in range(1, t + 1):
        time.sleep(1)
        xp.wr(xp.Fore.LIGHTBLUE_EX +
              ' - [' + '>' * i + '-' * (t - i) + '] sleep %s/%s s' % (i, t) + '\r')
        xp.fi()

    xp.fi(inline=False)


def get_dict_by_keys(source, keys: list or dict, default_none: bool = True):
    """
    Get a dict, by keys.

    :param source:
        json_string, dict, or a object
    :param keys:
        list or dict
    :param default_none:
        whether default value is None or ignore it, when the value does not exist.
        available only if keys is a list,
    :return:
        dict
    """
    r = {}
    if isinstance(source, str):
        try:
            import json
            source = json.loads(source)
        except Exception:
            return r
        return get_dict_by_keys(source, keys=keys, default_none=default_none)
    elif isinstance(source, dict):
        if isinstance(keys, list):
            for key in keys:
                if key in source.keys():
                    r[key] = source[key]
                else:
                    if default_none: r[key] = None
        else:
            for key, value in keys.items():
                if key in source.keys():
                    r[key] = source[key]
                else:
                    r[key] = value
    else:
        if isinstance(keys, list):
            for key in keys:
                if default_none:
                    r[key] = getattr(source, key, None)
                elif hasattr(source, key):
                    r[key] = getattr(source, key)
        else:
            for key, value in keys.items():
                r[key] = getattr(source, key, value)
    return r


def strip_in_list(the_list):
    r = []
    for value in the_list:
        if isinstance(value, str):
            r.append(value.strip())
        else:
            r.append(value)
    return r


def remove_in_list(the_list: list, ele=None):
    ele = ele or ['', None]
    if isinstance(ele, list):
        for e in ele:
            while e in the_list:
                the_list.remove(e)
    else:
        while ele in the_list:
            the_list.remove(ele)

    return the_list


def strip_and_remove_in_list(the_list: list, ele=None):
    the_list = strip_in_list(the_list=the_list)
    the_list = remove_in_list(the_list=the_list, ele=ele)
    return the_list
