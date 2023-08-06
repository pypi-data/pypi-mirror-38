# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import unittest
from jnius.reflect import autoclass

def py2_decode(str):
    # <AK> added
    return str.decode('utf-8') if sys.version_info < (3, 0) else str


class ImplementationTest(unittest.TestCase):

    def test_println(self):
        # System.out.println implies recursive lookup, and j_self assignation.
        # It was crashing during the implementation :/
        System = autoclass('java.lang.System')
        System.out.println('')

    def test_printf(self):
        System = autoclass('java.lang.System')
        System.out.printf('hi\n')
        System.out.printf('hi %s %s\n', 'jnius', 'other string')

    def test_unicode(self):
        System = autoclass('java.lang.System')
        System.out.printf(u'é')

        Stack = autoclass('java.util.Stack')
        stack = Stack()
        emoji = u'\U0001F602'
        stack.push(emoji)
        popped = stack.pop()
        popped = py2_decode(popped)  # <AK> chanded to use of py2_decode
        self.assertEquals(emoji, popped)
