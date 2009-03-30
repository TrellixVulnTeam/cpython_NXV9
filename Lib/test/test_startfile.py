# Ridiculously simple test of the os.startfile function for Windows.
#
# empty.vbs is an empty file (except for a comment), which does
# nothing when run with cscript or wscript.
#
# A possible improvement would be to have empty.vbs do something that
# we can detect here, to make sure that not only the os.startfile()
# call succeeded, but also the the script actually has run.

import unittest
from test import test_support
import os
from os import path

startfile = test_support.get_attribute(os, 'startfile')


class TestCase(unittest.TestCase):
    def test_nonexisting(self):
        self.assertRaises(OSError, startfile, "nonexisting.vbs")

    def test_nonexisting_u(self):
        self.assertRaises(OSError, startfile, u"nonexisting.vbs")

    def test_empty(self):
        empty = path.join(path.dirname(__file__), "empty.vbs")
        startfile(empty)
        startfile(empty, "open")

    def test_empty_u(self):
        empty = path.join(path.dirname(__file__), "empty.vbs")
        startfile(unicode(empty, "mbcs"))
        startfile(unicode(empty, "mbcs"), "open")

def test_main():
    test_support.run_unittest(TestCase)

if __name__=="__main__":
    test_main()
