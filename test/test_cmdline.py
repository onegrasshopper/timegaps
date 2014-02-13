# -*- coding: utf-8 -*-
# Copyright 2014 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals
import os
import sys
import logging
from py.test import raises, mark
from clitest import CmdlineInterfaceTest, CmdlineTestError, WrongExitCode


RUNDIRTOP = "./cmdline-test"
TIMEGAPS_NAME = "../../../timegaps.py"
PYTHON_EXE = "python"
WINDOWS = sys.platform == "win32"


class CmdlineInterfaceTestUnix(CmdlineInterfaceTest):
    rundirtop = RUNDIRTOP


class CmdlineInterfaceTestWindows(CmdlineInterfaceTest):
    shellpath = "cmd.exe"
    rundirtop = RUNDIRTOP
    shellscript_ext = ".bat"


CLITest = CmdlineInterfaceTestUnix
if WINDOWS:
    CLITest = CmdlineInterfaceTestWindows


logging.basicConfig(
    format='%(asctime)s,%(msecs)-6.1f %(funcName)s# %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger("test_cmdline")
log.setLevel(logging.DEBUG)


class Base(object):
    """Implement methods shared by all test classes.
    """

    def setup_method(self, method):
        name = "%s_%s" % (type(self).__name__, method.__name__)
        self.cmdlinetest = CLITest(name)

    def teardown_method(self, method):
        pass

    def run(self, arguments_unicode, expect_rc=0):
        cmd = "%s %s %s" % (PYTHON_EXE, TIMEGAPS_NAME, arguments_unicode)
        log.info("Test command:\n%s" % cmd)
        self.cmdlinetest.run(cmd_unicode=cmd, expect_rc=expect_rc)


class TestBasic(Base):
    """Test basic functionality.
    """

    def test_invalid_itempath_1(self):
        self.run("-v days5 nofile", 1)


