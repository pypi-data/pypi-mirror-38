#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _mac_appify.app import App


class Code:
    """Mac app generator from a shell script source"""
    __readme__ = ["__init__","appify"]
    _string = None

    def __init__(self, string):
        """init from string"""
        self.string = string

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, value):
        valid = value.splitlines() and value.splitlines()[0].find("#!") == 0
        if not valid:
            raise ValueError("shebang required:\n%s" % value)
        self._string = value

    def appify(self, app, image=None):
        """create Mac app"""
        App(path=app, code=self.string, image=image).create()
