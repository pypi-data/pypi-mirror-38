from __future__ import print_function

import sys

from datetime import datetime


class Color:
    RED = "\033[1;31m"
    ORANGE = "\033[1;33m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GRAY = "\033[2;37m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"


class Verbosity:
    DEBUG = 1
    DEFAULT = 0
    ERROR = -1
    NO_OUTPUT = -2


class Logger:
    def __init__(self, verbosity=Verbosity.DEFAULT, out=sys.stdout, err=sys.stderr):
        self.verbosity = verbosity
        self.out = out
        self.err = err

    @staticmethod
    def get_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log(self, tag, color, message, file=None):
        if file is None:
            file = self.out
        print(u"{}[{}]{} [{}] {}".format(color,
                                         tag,
                                         Color.RESET,
                                         self.get_time(),
                                         message), file=file)

    def debug(self, message):
        if self.verbosity >= Verbosity.DEBUG:
            self._log("DEBUG", Color.CYAN, message)

    def default(self, message):
        if self.verbosity >= Verbosity.DEFAULT:
            self._log("SPIP", Color.GREEN, message)

    def error(self, message):
        if self.verbosity >= Verbosity.ERROR:
            self._log("ERROR", Color.RED, message, file=self.err)

    def always(self, message):
        if self.verbosity > Verbosity.NO_OUTPUT:
            print(u"{}".format(message), file=self.out)
