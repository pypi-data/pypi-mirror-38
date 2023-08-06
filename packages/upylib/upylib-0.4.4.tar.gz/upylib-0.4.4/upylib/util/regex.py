#!/usr/bin/env python3
# -*- coding:utf-8 -*-⏎
from __future__ import print_function
import sys
import re

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if sys.version_info<(3,0,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def regex_replace(s, patt, rep):
    res = re.search(patt, s)
    if res is None:
        return s

    s = rep
    for i in range(1,9):
        var = "${%d}" % i
        if var in s:
            s = s.replace( var, res.group(i) )

    return s

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def test():
    """
    if len(sys.argv) != 3:
        print("usage: %s fn-in fn-out" % sys.argv[0])
        return False
    """
    s = "/banana/apple/cup (2018)/"
    print(s)

    patt = "/(.*)(.*)"
    print(patt)

    out = regex_replace(s, patt, "${1}\n${2}")
    print(out)

    patt = "/(.*)(\\d{4})"
    out = regex_replace(s, patt, "${1}\n${2}")
    print(out)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if __name__ == "__main__":
    test()

