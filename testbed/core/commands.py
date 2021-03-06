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
Contains functionality common to extensions.
"""
import sys
import logging
import importlib
import pkgutil
import argparse
import traceback
import testbed.settings
import testbed.core.logger


def logger_create():
    """ Create logger for tbd application. """
    console = logging.StreamHandler()
    formatter = logging.Formatter(testbed.settings.FMT)
    console.setFormatter(formatter)
    logger = logging.getLogger("")
    logger.addHandler(console)
    logger.setLevel(logging.WARNING)

    return logger


LOGGER = logger_create()


def args_process(args):
    """ Process any generic parameters. """

    if args.verbose == 1:
        LOGGER.setLevel(level=logging.INFO)
        LOGGER.info("verbosity level set to INFO")
    elif args.verbose > 1:
        LOGGER.setLevel(level=logging.DEBUG)
        LOGGER.info("verbosity level set to DEBUG")

    if args.database:
        ##
        # Database has been set.
        import testdb.router
        testdb.router.DefaultRouter.set_db(args.database)

    LOGGER.debug(args)
    args.func(args)


def argparser():
    """ Create top level argument parser. """

    arg_parser = argparse.ArgumentParser(prog="tbd")
    arg_parser.add_argument('--version', action="version",
                            version=testbed.__version__)
    arg_parser.add_argument('--verbose', '-v', required=False, action="count",
                            help="enable debug verbosity.")
    arg_parser.add_argument('--database', '-d', default=None,
                            required=False,
                            help="specify database.")
    return arg_parser


def onerror(name):
    """ Show module that fails to load. """
    LOGGER.error("importing module %s", name)
    _, _, trback = sys.exc_info()
    traceback.print_tb(trback)


def extensions_find(arg_parser):
    """ Look for command extensions. """

    subparser = arg_parser.add_subparsers(
        title="subcommands", description="Valid subcommands",
        help="Each subcommands supports --help for additional information.")

    for package in testbed.settings.PLUGINS:
        LOGGER.debug("loading commands %s", package)

        package = importlib.import_module(package)
        for _, module, ispkg in pkgutil.walk_packages(package.__path__,
                                                      package.__name__ + ".",
                                                      onerror=onerror):
            ##
            # only include commands from commands.py files.
            if ispkg or not module.endswith("commands"):
                continue
            LOGGER.debug("  loading commands from %s", module)
            module = importlib.import_module(module)
            try:
                module.add_subparser(subparser)
            except AttributeError, arg:
                ##
                # This means that the module is missing the add method.
                # All modules identified in settings to extend CLI
                # must have an add method
                LOGGER.error("adding subparser for %s.%s", package, module)
                LOGGER.exception(arg)


def main():
    """ Entry point for parsing tbd arguments. """
    arg_parser = argparser()
    extensions_find(arg_parser)
    return arg_parser
