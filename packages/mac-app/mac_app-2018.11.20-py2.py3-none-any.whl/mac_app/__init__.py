#!/usr/bin/env python
# -*- coding: utf-8 -*-
import exit
import mac_appify
import mdfind
import mkalias
import os
import plistlib
import public
import shutil
import sys
import time


"""
path/to/<name>.py                                 class Name(mac_app.App)

output:
~/Applications/.appify/<name>.app                 (customizable)

app logs:
~/Library/Logs/Applications/<name>/out.log        (customizable)
~/Library/Logs/Applications/<name>/err.log        (customizable)

app files:
<name>.app/Contents/MacOS/executable              bash wrapper (hack to keep app visible)
<name>.app/Contents/MacOS/launchd.plist           launchd.plist
<name>.app/Contents/MacOS/run.py                  (your class file)
"""

APPLICATIONS = os.path.join(os.environ["HOME"], "Applications")
LOGS = os.path.join(os.environ["HOME"], "Library/Logs/Applications")
CODE = """#!/usr/bin/env bash

# LaunchAgent required to keep app visible in Dock
set "${0%/*}"/launchd.plist
trap "launchctl unload '$1'" EXIT
PlistBuddy() { /usr/libexec/PlistBuddy "$@"; }
PlistBuddy -c "Delete WorkingDirectory" -c "Add WorkingDirectory string ${0%/*}" "$1"

Label="$(PlistBuddy -c "Print Label" "$1")"
# logs must exists or launchd will create logs with root permissions
logs="$(PlistBuddy -c "Print StandardErrorPath" -c "Print StandardOutPath" "$1")"
dirs="$(echo "$logs" | grep / | sed 's#/[^/]*$##' | uniq)"
( IFS=$'\\n'; set -- $dirs; [ $# != 0 ] && mkdir -p "$@" )

launchctl unload "$1" 2> /dev/null; launchctl load "$1"
while :; do sleep 0.3 && launchctl list "$Label" | grep -q PID || exit 0; done
"""


@public.add
class App:
    """Mac app generator"""
    __readme__ = ["atexit", "run", "appify", "mkalias", "sleep", "app_name", "app_path", "app_script", "app_stderr", "app_stdout", "app_image"]
    _app_name = None
    _app_image = None
    _app_script = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)
        if ".app/" in self.app_script:
            exit.register(self.atexit)

    def atexit(self):
        """executed at termination. override this method"""

    def run(self):
        """main function. you MUST override this method"""
        raise NotImplementedError

    @property
    def app_name(self):
        """app name. default is class name
app name concepts:
1)   custom name self._app_name with @app_name.setter
2)   class name self.__class__.__name__.lower().replace("_", "-")
3)   module name (os.path.splitext(os.path.basename(self.app_script))[0].replace("_", "-"))
        """
        if self._app_name:
            return self._app_name
        return self.__class__.__name__.lower().replace("_", "-")

    @app_name.setter
    def app_name(self, name):
        self._app_name = name

    @property
    def app_script(self):
        """source script path. default is class module file"""
        if self._app_script:
            return self._app_script
        return sys.modules[self.__class__.__module__].__file__

    @app_script.setter
    def app_script(self, path):
        self._app_script = path

    @property
    def app_path(self):
        """app path. default is `~/Applications/.appify/<name>.app`"""
        return os.path.join(APPLICATIONS, ".appify", "%s.app" % self.app_name)

    @property
    def appified(self):
        return os.path.exists(self.app_path)

    def rm_app(self):
        if os.path.exists(self.app_path):
            shutil.rmtree(self.app_path)
        return self

    @property
    def app_image(self):
        """app image. default is `mdfind kMDItemFSName=<name>.png` result"""
        if self._app_image:
            return self._app_image
        filename = "%s.png" % self.app_name
        matches = mdfind.mdfind(["kMDItemFSName=%s" % filename])
        if matches and os.path.exists(matches[0]):
            return matches[0]

    @app_image.setter
    def app_image(self, path):
        self._app_image = path

    @property
    def app_stdout(self):
        """stdout path. default is `~/Library/Logs/Applications/<name>/out.log`"""
        return os.path.join(LOGS, self.app_name, "out.log")

    @property
    def app_stderr(self):
        """stderr path. default is `~/Library/Logs/Applications/<name>/err.log`"""
        return os.path.join(LOGS, self.app_name, "err.log")

    def copy_script(self):
        dst = os.path.join(self.app_path, "Contents", "MacOS", "run.py")
        shutil.copy(self.app_script, dst)
        return self

    def appify(self):
        """create Mac app"""
        if ".app/" not in os.getcwd():
            mac_appify.Code(CODE).appify(self.app_path, self.app_image)
            self.copy_script()
            self.create_agent()
        return self

    def create_agent(self):
        Label = "%s.app" % self.app_name
        """
`bash -l` load your environment variables
        """
        ProgramArguments = ["bash", "-l", "-c", "python -u run.py"]
        data = dict(Label=Label, ProgramArguments=ProgramArguments, RunAtLoad=True, StandardOutPath=self.app_stdout, StandardErrorPath=self.app_stderr)
        path = os.path.join(self.app_path, "Contents", "MacOS", "launchd.plist")
        plistlib.writePlist(data, path)

    def mkalias(self, dst):
        """make Mac alias to app"""
        mkalias.mkalias(self.app_path, dst)
        os.utime(os.path.dirname(dst), None)  # refresh Dock icon
        return self

    def sleep(self, seconds):
        """suspend app for the given number of seconds"""
        time.sleep(seconds)
        return self

    def __str__(self):
        return '<App "%s">' % self.app_path

    def __repr__(self):
        return self.__str__()
