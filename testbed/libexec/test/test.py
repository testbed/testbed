# (c) 2015 Mark Hamilton, <mark.lee.hamilton@gmail.com>
#
# This file is part of testbed
#
# Testbed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Testbed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Testdb.  If not, see <http://www.gnu.org/licenses/>.
"""
Test test functionality.
"""
import argparse
from django.test import TestCase
from testdb.models import Testsuite
from testdb.models import Test
from . import commands
from testbed.libexec import testplan


class TestTestCase(TestCase):
    """ Tests for Django backend.

    These test must derive from django.test.TestCase. """

    @staticmethod
    def parser_create():
        """ Create sub parser. """

        arg_parser = argparse.ArgumentParser(prog="tbd")
        subparser = arg_parser.add_subparsers(title="subcommands")
        commands.add_subparser(subparser)
        return arg_parser

    def test_commands_add(self):
        """ Add a test. """

        parser = TestTestCase.parser_create()

        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite1",
                                   testplan.api.ORDER_NEXT)
        args = parser.parse_args("test add build1 testsuite1 test1".split())
        args.func(args)

        args = parser.parse_args("test add build1 testsuite1 test2".split())
        args.func(args)

        names = [item.name.name for item in Testsuite.contains("default",
                                                               "testsuite1")]
        self.assertTrue(len(names) == 1)

        names = [item.name.name for item in Test.filter("testsuite1")]
        self.assertTrue(len(names) == 2)

        self.assertTrue(any("test1" in name for name in names))
        self.assertTrue(any("test2" in name for name in names))

    def test_context_add(self):
        """ Add a testsuite ignoring context.

        Testplan is created called testplan1. Adding a testsuite which is
        not part of the default testplan should still work.
        """

        testplan.api.get_or_create("testplan.testplan1", "testsuite1",
                                   testplan.api.ORDER_NEXT)

        parser = TestTestCase.parser_create()

        cmd = "test add build1 testsuite1 test1 --context testschedule1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        tests = Test.filter("testsuite1")
        self.assertTrue(len(tests) == 1)

        names = [item.name.name for item in tests]
        self.assertTrue("test1" in names)

        names = [item.testsuite.name.name for item in tests]
        self.assertTrue("testsuite1" in names)

        tests = Test.filter("testschedule1")
        self.assertTrue(len(tests) == 1)

        context = [item.testsuite.context.name for item in tests]
        self.assertTrue("testschedule1" in context)

        names = [item.name.name for item in tests]
        self.assertTrue("test1" in names)

        names = [item.testsuite.name.name for item in tests]
        self.assertTrue("testsuite1" in names)

    def test_list_filter(self):
        """ Add a test to testsuite. """
        parser = TestTestCase.parser_create()

        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite2",
                                   testplan.api.ORDER_NEXT)
        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite3",
                                   testplan.api.ORDER_NEXT)

        cmd = "test add build1 testsuite2 test1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "test add build1 testsuite3 test2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "test add build1 testsuite3 test3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        tests = Test.filter("testsuite3")
        items = [item for item in tests]
        self.assertTrue(len(items) == 2)
        names = [item.name.name for item in items]
        self.assertTrue(any("test2" in name for name in names))
        self.assertTrue(any("test3" in name for name in names))
