#!/usr/bin/env python
import imp
import os
import public
import python_files


@public.add
def source(name, path):
    """load python file"""
    return imp.load_source(name, path)


@public.add
def sources(name, path):
    """load python files from dir"""
    modules = []
    find = list(python_files.find(path))
    for f in find:
        relpath = f.replace("%s/" % os.path.dirname(path), "")
        pyname = relpath.replace("__init__.py", "")[:-3].replace("/", ".")
        _name = pyname
        if name:
            _name = "%s.%s" % (name, pyname)
        module = source(_name, f)
        modules.append(module)
    return modules
