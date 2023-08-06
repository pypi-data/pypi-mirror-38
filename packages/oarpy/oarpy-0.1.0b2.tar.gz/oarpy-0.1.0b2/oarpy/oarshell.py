# -*- coding: utf-8 -*-
#
#   Copyright (C) 2018 European Synchrotron Radiation Facility, Grenoble, France
#
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

__authors__ = ["W. De Nolf"]
__license__ = "MIT"


import os
import subprocess
import json
import logging
import shlex

logger = logging.getLogger(__name__)


def _execute(args, **kwargs):
    logger.debug('Subprocess: {}'.format(' '.join(args)))
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    logger.debug('stdout: {}'.format(out))
    logger.debug('stderr: {}'.format(err))
    if out:
        out = out.decode()
    if err:
        err = err.decode()
    return out, err, proc.returncode


def installed(*args):
    try:
        devnull = open(os.devnull)
        _execute(args, stdout=devnull, stderr=devnull)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def execute(*args):
    try:
        return _execute(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as e:
        return None, None, e.errno


def oarinstalled():
    return installed('oarsub', '--version')


def executejson(cmd, *args):
    """

    :param str cmd:
    :return tuple: out(dict), err(str or None), exitcode(int)
    """
    out, err, code = execute(cmd, '-J', *args)
    if out:
        try:
            start = out.index('{')
            stop = out.index('}')
        except ValueError:
            out = {}
        else:
            out = json.loads(out[start:stop+1])
    else:
        out = {}
    return out, err, code


def oarstat(*args):
    """

    :return tuple: out(dict), err(str or None), exitcode(int)
    """
    out, err, code = execute('oarstat', '-J', *args)
    if out:
        out = json.loads(out)
    else:
        out = {}
    return out, err, code


def oarjobstat(jobid, *args):
    """oarstat for a single job

    :param int jobid:
    :return tuple: out(str or dict or None), err(str or None), exitcode(int)
    """
    jobid = str(jobid)
    out, err, code = oarstat('-j', jobid, *args)
    if out:
        out = out.get(jobid, None)
    else:
        out = None
    return out, err, code


def oarsub(*args):
    """

    :return tuple: out(str or None), err(str or None), exitcode(int)
    """
    out, err, code = execute('oarsub', '-J', *args)
    if out:
        try:
            start = out.index('{')
            stop = out.index('}')
        except ValueError:
            out = 0
        else:
            out = json.loads(out[start:stop+1]).get('job_id', 0)
    else:
        out = 0
    return out, err, code


def jobstatus(jobid):
    """
    :param int jobid:
    :return str or None: * None: means job is not registered
                         * Hold: not scheduled (needs to be resumed)
                         * Waiting: scheduled for execution
                         * Suspended: running process is suspended
                            (needs to be resumed)
                         * Launching: process is starting
                         * Running: process is running
                         * Resuming: resuming after hold or suspended
                         * Finishing: process is stopping
                         * Terminated: process finished successfully
                         * Error: process finished successfully
    """
    out, _, code = oarjobstat(jobid, '-s')
    if code:
        return None
    else:
        return out


def jobstats(jobid):
    """
    :param int jobid:
    :return tuple: out(str or None), err(str or None), exitcode(int)
    """
    out, err, code = oarjobstat(jobid, '-f')
    if not isinstance(out, dict):
        out = {}
    return out, err, code


def jobresume(jobid):
    return execute('oarresume', str(jobid))


def jobhold(jobid):
    # Not permissions to hold running job with the -r option
    return execute('oarhold', str(jobid))


def jobdel(jobid, signal=None):
    args = []
    if signal:
        args = ['-s', signal]
    return execute('oardel', str(jobid), *args)


def cli_args2str(*cli_arguments):
    return subprocess.list2cmdline(cli_arguments)


def cli_str2args(cmd):
    return tuple(shlex.split(cmd))


def cli_getarg(cli_arguments, flag):
    if flag in cli_arguments:
        i = cli_arguments.index(flag)
        ret = cli_arguments[i+1]
        if ret.startswith('-'):
            return ''
        else:
            return ret
    else:
        return ''
