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
from ..oarresource import Resource


class test_oarresource(unittest.TestCase):
    def test_cores(self):
        self.assertFalse(Resource())
        self.assertTrue(Resource(core=1))
        self.assertEqual(Resource(nodes=1).cores, 1)
        self.assertEqual(Resource(cpu=1).cores, 1)
        self.assertEqual(Resource(core=1).cores, 1)

    def test_to_cli(self):
        res = Resource(nodes=1, cpu=2, core=2, gpu=True, mem_core_mb=8000)
        cli = '-l nodes=1/cpu=2/core=2 -p "gpu=\'YES\' and mem_core_mb>=8000"'
        self.assertEqual(cli, res.cli_string)
        self.assertEqual(res.cores, 4)

    def test_from_cli(self):
        res = Resource()
        self.assertEqual(res, Resource.from_cli(res.cli_string))
        res = Resource(core=10)
        self.assertEqual(res, Resource.from_cli(res.cli_string))
        res = Resource(nodes=1, cpu=2, core=2, gpu=True)
        self.assertEqual(res, Resource.from_cli(res.cli_string))
        res = Resource(nodes=1, cpu=2, core=2, mem_core_mb=8000)
        self.assertEqual(res, Resource.from_cli(res.cli_string))
        res = Resource(nodes=1, cpu=2, core=2, gpu=True, mem_core_mb=8000)
        self.assertEqual(res, Resource.from_cli(res.cli_string))


def test_suite():
    """Test suite including all test suites"""
    testSuite = unittest.TestSuite()
    testSuite.addTest(test_oarresource("test_cores"))
    testSuite.addTest(test_oarresource("test_to_cli"))
    testSuite.addTest(test_oarresource("test_from_cli"))
    return testSuite


if __name__ == '__main__':
    import sys

    mysuite = test_suite()
    runner = unittest.TextTestRunner()
    if not runner.run(mysuite).wasSuccessful():
        sys.exit(1)
