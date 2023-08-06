##############################################################################
#
# Copyright (c) 2007-2013 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Currency Test Setup
"""
import re
import unittest
import doctest

from zope.testing import renormalizing


checker = renormalizing.OutputChecker([
    # Python 3 unicode removed the "u".
    (re.compile("u('.*?')"),
     r"\1"),
    (re.compile('u(".*?")'),
     r"\1"),
    # Normalize the module name in exceptions:
    (re.compile(r'z3c\.currency\.interfaces\.'), r'')
    ])


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            'README.rst',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            checker=checker,
        ),
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
