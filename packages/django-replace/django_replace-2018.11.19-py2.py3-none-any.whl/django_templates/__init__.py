#!/usr/bin/env python
import os
import public


def _dirs(path):
    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            yield os.path.join(root, _dir)


@public.add
def find(path):
    """return list with `templates/` folders"""
    templates = []
    for _dir in _dirs(path):
        if os.path.basename(_dir) == "templates":
            templates.append(_dir)
    return templates
