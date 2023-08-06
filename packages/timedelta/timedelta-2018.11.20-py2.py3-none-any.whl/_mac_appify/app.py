#!/usr/bin/env python
import os
import plistlib
import chmod
import public
import runcmd

"""
path/to/name.app/Contents/MacOS/executable
path/to/name.app/Contents/Resources/Icon.icns
path/to/name.app/Contents/Info.plist
"""


def _mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class App:
    """Mac app generator"""
    __readme__ = ["create"]
    path = None
    _code = None
    image = None

    def __init__(self, path, code, image=None):
        self.path = path
        self.code = code
        self.image = image

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        valid = value.splitlines() and value.splitlines()[0].find("#!") == 0
        if not valid:
            raise ValueError("shebang required:\n%s" % value)
        self._code = value

    def create_executable(self):
        path = os.path.join(self.path, "Contents", "MacOS", "executable")
        _mkdir(os.path.dirname(path))
        open(path, "w").write(self.code)
        chmod.make.executable(path)

    def create_info(self):
        path = os.path.join(self.path, "Contents", "Info.plist")
        _mkdir(os.path.dirname(path))
        info = dict(CFBundleExecutable="executable")
        if self.image:
            info.update(CFBundleIconFile="Icon.icns")
        plistlib.writePlist(info, path)

    def create_icon(self):
        path = os.path.join(self.path, "Contents", "Resources", "Icon.icns")
        args = ["sips", "-s", "format", "icns", self.image, "--out", path]
        if self.image:
            _mkdir(os.path.dirname(path))
            runcmd.run(args)._raise()

    def create(self):
        """create app"""
        self.create_info()
        self.create_executable()
        self.create_icon()
        self.refresh()
        return self

    def refresh(self):
        """remove .DS_Store and touch folder"""
        for folder in [self.path, os.path.dirname(self.path)]:
            try:
                f = os.path.join(folder, ".DS_Store")
                if os.path.exists(f):
                    os.unlink(f)
                os.utime(folder, None)
            except PermissionError:
                pass
        return self

    def mkalias(self, path):
        # todo
        return self
