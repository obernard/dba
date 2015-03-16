#!/usr/env/bin python

import json

from Cheetah.Template import Template

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

with open('dw.json') as f:
    searchList = json.load(f, object_hook=_decode_dict)

with open('createDB.tmpl') as f:
    sqltmpl = f.read()

with open('datadict.tmpl') as f:
    datadicttmpl = f.read()

sqlscript = Template(sqltmpl, searchList)
print(sqlscript)

datadict = Template(datadicttmpl, searchList)
print(datadict)
