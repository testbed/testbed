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
Test testsuite functionality.
"""
import argparse
from django.test import TestCase
from testdb.models import KVP
from . import commands


class TestsuiteTestCase(TestCase):
    """ Tests for Django backend.
    These test must derive from django.test.TestCase. """

    @staticmethod
    def parser_create():
        """ Create sub parser. """
        arg_parser = argparse.ArgumentParser(prog="tbd")
        subparser = arg_parser.add_subparsers(title="subcommands")
        commands.add_subparser(subparser)
        return arg_parser

    def test_kvp_add(self):
        """ Add a testsuite. """
        parser = TestsuiteTestCase.parser_create()

        args = parser.parse_args("kvp add key1 value1.1".split())
        self.assertTrue(args.func(args))

        args = parser.parse_args("kvp add key1 value1.2".split())
        self.assertTrue(args.func(args))

    def test_kvp_strict(self):
        """ Add a testsuite. """
        parser = TestsuiteTestCase.parser_create()

        args = parser.parse_args("kvp add key1 value1.1".split())
        self.assertTrue(args.func(args))

        args = parser.parse_args("kvp type key1 STRICT".split())
        self.assertTrue(args.func(args))

        with self.assertRaises(KVP.DoesNotExist):
            KVP.get_or_create("key1", "value1.2")
