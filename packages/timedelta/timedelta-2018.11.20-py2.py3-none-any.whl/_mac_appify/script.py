#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _mac_appify.code import Code


class Script:
    """Mac app generator from a shell script file"""
    __readme__ = ["__init__","appify"]
    path = None

    def __init__(self, path):
        """init from script file"""
        self.path = path

    def appify(self, app, image=None):
        """create Mac app"""
        code = open(self.path).read()
        return Code(code).appify(app, image)
