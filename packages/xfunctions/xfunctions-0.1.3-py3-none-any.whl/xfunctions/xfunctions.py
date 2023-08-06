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


def get_dict_by_keys(source, keys: list, default_none: bool = True):
    r = {}
    if isinstance(source, dict):
        for key in keys:
            if key in source.keys():
                r[key] = source[key]
            else:
                if default_none: r[key] = None
    elif isinstance(source, str):
        import json
        try:
            source = json.loads(source)
        except Exception:
            pass
        return get_dict_by_keys(source, keys=keys, default_none=default_none)
    else:
        for key in keys:
            if default_none:
                r[key] = getattr(source, key, None)
            elif hasattr(source, key):
                r[key] = getattr(source, key)
        pass
    return r
