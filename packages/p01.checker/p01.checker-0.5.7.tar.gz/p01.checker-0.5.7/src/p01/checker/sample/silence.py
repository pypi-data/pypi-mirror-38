##############################################################################
#
# Copyright (c) 2012 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""Sample module supporting p01.checker.silence

$Id: silence.py 4936 2018-11-09 15:46:34Z roger.ineichen $
"""

class Foo(object):
    """A sample class forcing pyflake troubles"""

    def undefined_name(self):
        foo = False
        return bar

    def non_ascii_silence(self):
        return u'ö' # p01.checker.silence

    def non_ascii(self):
        return u'ö'
