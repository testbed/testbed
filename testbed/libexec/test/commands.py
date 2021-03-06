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
CLI for tests.
"""
import logging
from testbed.libexec import testsuite

LOGGER = logging.getLogger(__name__)


def do_add_test(args):
    """ Add a test. """

    from testdb import models

    LOGGER.info("adding test %s.%s", args.testsuite, args.name)
    (testsuite1, _) = testsuite.api.add_testsuite(args.testplan, args.context,
                                                  args.testsuite, args.build,
                                                  [])
    models.Test.get_or_create(testsuite1, args.name, args.status, [])


def do_list_test(args):
    """ List testsuites based on search criteria. """

    from testdb import models
    LOGGER.info("listing tests")
    tests = models.Test.filter(args.filter)
    for test in tests:
        print test


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    ##
    # Adding a test requires a testsuite.
    #
    # test add <testsuite> <name>
    parser = subparser.add_parser("test", help=__doc__)
    subparser = parser.add_subparsers()

    parser = subparser.add_parser("add", help="add a test",
                                  description="add a test")
    parser.set_defaults(func=do_add_test)
    parser.add_argument("build", type=str, help="Build id")
    parser.add_argument("testsuite", type=str, help="Testsuite name.")
    parser.add_argument("name", type=str, help="test name")
    parser.add_argument("--status", default="pass", type=str,
                        help="Test status.")
    parser.add_argument("--context", default="default",
                        help="Testsuite context.")
    parser.add_argument("--testplan", default=None, help="Testsuite context.")

    parser = subparser.add_parser("list",
                                  description="List tests in their testsuit.",
                                  help="List test.")
    parser.add_argument("--filter", type=str, help="Filter testsuites")
    parser.set_defaults(func=do_list_test)
    return subparser
