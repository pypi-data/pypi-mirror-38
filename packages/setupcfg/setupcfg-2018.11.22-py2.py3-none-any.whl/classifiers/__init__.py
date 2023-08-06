#!/usr/bin/env python
import cls
import public
import recursion_detect
import write

"""
https://pypi.org/pypi?%3Aaction=list_classifiers
"""


def _string(value):
    try:
        return isinstance(value, basestring)
    except NameError:
        return isinstance(value, str)


def _valid(value):
    return _string(value) and " :: " in value


def _iterable_values(value):
    value = list(value)  # store generator/list/set/tuple values to variable
    for v in value:
        if not _valid(v):
            return []
    return list(value)


def _values(value):
    if _string(value):
        if _valid(value):
            return [value]
    if hasattr(value, "__iter__"):
        return _iterable_values(value)
    return []


@public.add
class Classifiers:
    """classifiers.txt generator"""
    __readme__ = ["__init__", "load", "save", "search", "classifiers", "__contains__", "__iter__"]
    custom_classifiers = []

    def __init__(self, path=None, classifiers=None):
        """init from file with classifiers or/and classifiers list"""
        if path:
            self.load(path)
        if classifiers:
            self.custom_classifiers = classifiers

    def load(self, path):
        """load classifiers from file"""
        for line in open(path).read().splitlines():
            if _valid(line):
                self.append(line)
        return self

    def save(self, path):
        """save classifiers to file"""
        write.write(path, "\n".join(self.classifiers()))
        return self

    def append(self, classifier):
        """append classifier"""
        for line in classifier.splitlines():
            if line:
                self.custom_classifiers.append(line)
        self.custom_classifiers = list(sorted(self.custom_classifiers))
        return self

    def search(self, classifier):
        """search classifier"""
        result = []
        for item in self.classifiers():
            if str(classifier).lower() in item.lower():  # case insensitive
                result.append(item)
        return list(sorted(result))

    def classifiers(self):
        """return classifiers list (from attrs and properties with :: )"""
        result = list(self.custom_classifiers)  # list() required - copy items
        for key in cls.attrs(self.__class__):  # attrs
            result += _values(getattr(self, key))
        # prevent properties recursion
        if recursion_detect.depth() > 0:
            return result
        for key in cls.properties(self.__class__):  # properties
            result += _values(getattr(self, key))
        return list(sorted(set(filter(None, result))))

    def __contains__(self, classifier):
        """return True if classifier defined"""
        return bool(self.search(classifier))

    def __iter__(self):
        """iterate classifiers"""
        for classifier in self.classifiers():
            yield classifier

    def __getitem__(self, key):
        return self.search(key)

    def __len__(self):
        return len(self.classifiers())

    def __str__(self):
        return "\n".join(self.classifiers())

    def __repr__(self):
        return "<Classifiers (%s)>" % self.count
