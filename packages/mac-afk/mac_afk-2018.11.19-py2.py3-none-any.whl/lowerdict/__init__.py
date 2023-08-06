#!/usr/bin/env python
from isstring import isstring
import public


@public.add
def lowerdict(*args, **kwargs):
    """return dict with lowercase keys"""
    inputdict = dict(*args, **kwargs)
    resultdict = dict()
    for key, value in inputdict.items():
        if isstring(key):
            key = key.lower()
        resultdict[key] = value
    return resultdict
