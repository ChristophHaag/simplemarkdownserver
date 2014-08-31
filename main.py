#!/usr/bin/env python3

from bottle import route, run, template, post, request
import json
from functools import lru_cache
import os
import time

scriptpath = os.path.dirname(os.path.realpath(__file__))

def entryname(name):
    if name.endswith(".txt"):
        return name[:-4]
    else:
        return name

@lru_cache(maxsize=2048)
def fntime(fn):
    return time.ctime(os.path.getmtime(fn))

@lru_cache(maxsize=2048)
def timestr(fn):
    return "last modified: %s" % fntime(fn)

@lru_cache(maxsize=2048)
def getEntry(category,fn):
    entryfn = scriptpath + "/" + category + "/" + fn
    title = entryname(fn)
    with open(entryfn) as f:
        content = f.read()
    return title, content, timestr(entryfn)

@lru_cache()
def getCategories():
    categories = sorted([name for name in os.listdir(scriptpath)
                         if not name.startswith(".")
                         and os.path.isdir(os.path.join(scriptpath, name))])
    return categories

#TODO: sorting
@lru_cache()
def getEntries(category):
    e = sorted([name for name in os.listdir(scriptpath + "/" + category) if os.path.isfile(os.path.join(scriptpath + "/" + category, name))])
    return e

@route('/entry/<category>/<filename>')
def entry(category,filename):
    t, c, d = getEntry(category, filename)
    return template("markdown.tpl", title=t, content=c, date=d)

@route('/category/<filename>')
def cat(filename):
    s = "\n".join(["* [" + entryname(e) + " (" + timestr(scriptpath + "/" + filename + "/" + e) + ")](../entry/" + filename + "/" + e + ")" for e in getEntries(filename)])
    e = template("markdown.tpl", title="Category: " + filename, content=s)
    return e

@route('/')
def r():
    content = "\n".join(["* [" + c + "](./category/" + c + ")" for c in getCategories()])
    s = template("markdown.tpl", title="Overview", content=content)
    return s

run(host='0.0.0.0', port=8124, reloader=True, debug=True)