# -*- coding: utf-8 -*-


def ensure_unicode(obj):
    """Recursively encode the given ``obj`` to unicode.

    Credit should go out to Ben Darnell for this one since the code
    is a modification of the solution in tornado.

    :param obj: The object to walk through and encode contained values
    """
    if isinstance(obj, (unicode, type(None))):
        return obj

    if isinstance(obj, dict):
        items = obj.iteritems()
        return dict((ensure_unicode(k), ensure_unicode(v)) for k, v in items)
    elif isinstance(obj, (list, tuple)):
        return list(ensure_unicode(i) for i in obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    return obj
