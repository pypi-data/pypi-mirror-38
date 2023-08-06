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
import os
import tempfile
from time import sleep
import shutil

from .. import oarjob
from ..oarresource import Resource
from ..oarshell import oarinstalled


class test_oarjob(unittest.TestCase):
    def setUp(self):
        self.working_directory = tempfile.mkdtemp(dir=os.getcwd())

    def tearDown(self):
        shutil.rmtree(self.working_directory)

    def skipoar(self):
        if not oarinstalled():
            raise unittest.SkipTest("oar cli tools not available")

    def test_status(self):
        self.skipoar()
        job = oarjob.Job(1)
        with job.fixed_stats():
            self.assertTrue(job.exists)
            self.assertTrue(job.is_finished)
            self.assertFalse(job.is_running)
            self.assertFalse(job.is_waiting)
            self.assertFalse(job.is_intermediate)
            self.assertFalse(job.needsresume)
        self.assertEqual(job['state'], job.status)

    def test_jobfactory(self):
        self.skipoar()
        self.assertTrue(oarjob.JobFactory())
        self.assertTrue(oarjob.JobFactory(command='ls -all'))

        res = Resource(nodes=1, cpu=2, core=2, gpu=True, mem_core_mb=8000)
        info = oarjob.JobFactory(resource=res, command='ls -all', log_base='test')
        cli = "-O test.stdout -E test.stderr -l nodes=1/cpu=2/core=2 -p \"gpu='YES' and mem_core_mb>=8000\" \"ls -all\""
        self.assertEqual(cli, info.cli_string)

    def definition(self, seconds, name):
        command = 'python -c "from time import sleep\nfor i in range({}):\n print(i)\n sleep(1)"'
        resource = Resource(core=1, walltime={'seconds': seconds * 3})
        jobdef = oarjob.JobFactory(name=name, project='oarpy',
                                   resource=resource, command=command.format(seconds),
                                   working_directory=self.working_directory)
        output = list(range(seconds))
        return jobdef, output

    def _check_output(self, job, expected):
        output = [int(i) for i in job.stdout.split('\n') if i]
        self.assertEqual(output, expected)

    def test_immediate(self):
        self.skipoar()
        jobdef, expected = self.definition(5, 'immediate')
        job = jobdef.submit()
        self.assertEqual(job.definition, jobdef)
        job.wait(silent=True)
        self.assertEqual(job.exit_code, 0)
        self._check_output(job, expected)

    def test_notimmediate(self):
        self.skipoar()
        jobdef, expected = self.definition(5, 'notimmediate')
        job = jobdef.submit(hold=True)
        job.wait(states=('Hold', 'Suspended'), silent=True)
        job.resume()
        job.wait(silent=True)
        self.assertEqual(job.exit_code, 0)
        self._check_output(job, expected)

    def test_interrupt(self):
        self.skipoar()
        jobdef, expected = self.definition(60, 'interrupt')
        job = jobdef.submit()
        job.wait(states=('Running', 'Terminated', 'Error'), silent=True)
        sleep(5)
        job.interrupt()
        job.wait(silent=True)
        self.assertEqual(job.exit_code, None)

    def test_suspend(self):
        self.skipoar()
        jobdef, expected = self.definition(60, 'interrupt')
        job = jobdef.submit()
        job.wait(states=('Running', 'Terminated', 'Error'), silent=True)
        self.assertRaises(RuntimeError, job.suspend)
        # job.wait(states='Hold', silent=True)
        # job.resume()
        # job.wait(silent=True)
        # self.assertEqual(job.exit_code,0)
        # self._check_output(job,expected)


def test_suite():
    """Test suite including all test suites"""
    testSuite = unittest.TestSuite()
    testSuite.addTest(test_oarjob("test_status"))
    testSuite.addTest(test_oarjob("test_jobfactory"))
    testSuite.addTest(test_oarjob("test_immediate"))
    testSuite.addTest(test_oarjob("test_notimmediate"))
    testSuite.addTest(test_oarjob("test_interrupt"))
    testSuite.addTest(test_oarjob("test_suspend"))
    return testSuite


if __name__ == '__main__':
    import sys

    mysuite = test_suite()
    runner = unittest.TextTestRunner()
    if not runner.run(mysuite).wasSuccessful():
        sys.exit(1)
