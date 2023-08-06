# -*- coding: utf-8 -*-
#
#   Copyright (C) 2018 European Synchrotron Radiation Facility, Grenoble, France
#
#   Principal author:   Wout De Nolf (wout.de_nolf@esrf.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import unittest
from .. import oarshell


class test_utils(unittest.TestCase):

    def skipoar(self):
        if not oarshell.oarinstalled():
            raise unittest.SkipTest("oar cli tools not available")

    def test_installed(self):
        oarshell.oarinstalled()

    def test_oarstat(self):
        self.skipoar()
        out, err, code = oarshell.jobstats(1)
        self.assertTrue(isinstance(out, dict))

    def test_cli(self):
        args = '-p', "gpu=YES"
        cmd1 = oarshell.cli_args2str(*args)
        cmd2 = "-p gpu=YES"
        self.assertEqual(cmd1, cmd2)
        self.assertEqual(args, oarshell.cli_str2args(cmd2))

        args = '-p', "gpu='YES'"
        cmd1 = oarshell.cli_args2str(*args)
        cmd2 = "-p gpu='YES'"
        self.assertEqual(cmd1, cmd2)
        self.assertEqual(('-p', "gpu=YES"), oarshell.cli_str2args(cmd1))

        args = '-p', "gpu='YES' and mem_core_mb>=8000"
        cmd1 = oarshell.cli_args2str(*args)
        cmd2 = '-p "gpu=\'YES\' and mem_core_mb>=8000"'
        self.assertEqual(cmd1, cmd2)
        self.assertEqual(args, oarshell.cli_str2args(cmd2))


def test_suite():
    """Test suite including all test suites"""
    testSuite = unittest.TestSuite()
    testSuite.addTest(test_utils("test_installed"))
    testSuite.addTest(test_utils("test_oarstat"))
    testSuite.addTest(test_utils("test_cli"))
    return testSuite


if __name__ == '__main__':
    import sys

    mysuite = test_suite()
    runner = unittest.TextTestRunner()
    if not runner.run(mysuite).wasSuccessful():
        sys.exit(1)
