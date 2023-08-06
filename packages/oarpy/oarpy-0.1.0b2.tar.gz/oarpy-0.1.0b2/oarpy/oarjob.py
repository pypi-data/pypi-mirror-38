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

import logging
import errno
from contextlib import contextmanager
from time import sleep
import datetime
import sys
import os

from . import oarshell
from . import oarresource
from . import timeutils

logger = logging.getLogger()


class Job(object):
    """Manage existing jobs but does not create new jobs
    """

    _POSSIBLE_STATES = ('Launching', 'Resuming', 'Finishing', 'Terminated',
                        'Error', 'Running', 'Waiting', 'Hold', 'Suspended')
    """list all the possible state the job can take"""

    def __init__(self, jobid):
        """

        :param int jobid:
        """
        self._jobid = jobid
        self._fixed_stats = None
        """Used to store stats when using the `fixed_stats` context
        manager"""

    @property
    def jobid(self):
        return self._jobid

    @property
    def exists(self):
        return bool(self.status)

    @property
    def is_terminated(self):
        return self.status == 'Terminated'

    @property
    def has_error(self):
        return self.status == 'Error'

    @property
    def is_finished(self):
        return self.status in ['Terminated', 'Error']

    @property
    def is_running(self):
        return self.status == 'Running'

    @property
    def is_waiting(self):
        return self.status == 'Waiting'

    @property
    def is_intermediate(self):
        return self.status in ['Launching', 'Resuming', 'Finishing']

    @property
    def needsresume(self):
        return self.status in ['Hold', 'Suspended']

    @property
    def status(self):
        if self._fixed_stats:
            return self['state']
        else:
            if self.jobid is None:
                return None
            else:
                return oarshell.jobstatus(self.jobid)

    @property
    def stats(self):
        if self._fixed_stats:
            return self._fixed_stats
        else:
            if self.jobid is None:
                stats = {}
            else:
                stats, err, code = oarshell.jobstats(self.jobid)
                self._raise_if_error(err, code, 'Cannot retrieve job stats')
                self._parse_stats(stats)
            return stats

    @contextmanager
    def fixed_stats(self):
        first = not bool(self._fixed_stats)
        if first:
            self._fixed_stats = self.stats
        yield
        if first:
            self._fixed_stats = None

    def __getitem__(self, key):
        return self.stats.get(key, None)

    def wait(self, states=('Terminated', 'Error'), timeout=None, refresh=1,
             silent=False):
        """

        :param states: state or states we are waiting for
        :type states: str or tuple
        :param timeout: if not none, second before the timeout.
        :type timeout: int or None
        :param int refresh: time (in seconds) between two observations of the job
                            state
        :param silent: if False then write to stdout advancement ('.')
        """
        # make sure _until will always be iterable (deal with str, bytes...)
        _states = states
        if isinstance(_states, (tuple, list, dict)) is False:
            _states = (_states,)
        for _state in _states:
            if _state not in self._POSSIBLE_STATES:
                raise ValueError('%s is not a valid state. Unable to wait for it' % _state)

        _until = lambda: self.status in _states

        waited_time = 0
        newline = False
        while not _until():
            sleep(refresh)
            waited_time = waited_time + refresh
            if timeout is not None:
                if waited_time >= timeout:
                    logger.warning('wait on job %s has reach a timeout' % self.jobid)
                    return
            if not silent:
                sys.stdout.write('.')
                sys.stdout.flush()
                newline = True
        if newline:
            print('')

    @property
    def runtime(self):
        """Effective execution time, excluding queue time
        """
        dt = self._time_diff('stopTime', 'startTime')
        return max(dt, datetime.timedelta(seconds=0))

    @property
    def time_scheduled(self):
        """Time this job was scheduled, excluding queue and runtime
        """
        dt = self._time_diff('startTime', 'scheduledStart')
        return max(dt, datetime.timedelta(seconds=0))

    @property
    def time_enqueued(self):
        """Time this job was enqueue (not scheduled for execution)
        """
        dt = self._time_diff('scheduledStart', 'submissionTime')
        return max(dt, datetime.timedelta(seconds=0))

    @property
    def time_to_start(self):
        """Time until the job starts
        """
        dt = self._time_diff('startTime', timeutils.now())
        return max(dt, datetime.timedelta(seconds=0))

    @property
    def stderr_file(self):
        return self._std_file('stderr_file')

    @property
    def stdout_file(self):
        return self._std_file('stdout_file')

    @property
    def stderr(self):
        return self._std_read(self.stderr_file)

    @property
    def stdout(self):
        return self._std_read(self.stdout_file)

    def _std_file(self, filename):
        with self.fixed_stats():
            filename = self[filename]
            if os.path.dirname(filename):
                return filename
            else:
                return os.path.join(self.working_directory, filename)

    @staticmethod
    def _std_read(filename):
        try:
            with open(filename, mode='r') as f:
                return f.read()
        except IOError as e:
            if e.errno == errno.ENOENT:
                return None
            else:
                raise e

    def remove_logs(self):
        with self.fixed_stats():
            for f in [self.stderr_file, self.stdout_file]:
                try:
                    os.remove(f)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        pass
                    else:
                        raise e

    @property
    def exit_code(self):
        """

        :return: * None: interrupted by user
                 * ==0: success
                 * !=0: error
        """
        return self['exit_code']

    @property
    def name(self):
        return self['name']

    @property
    def project(self):
        return self['project']

    @property
    def command(self):
        return self['command']

    @property
    def working_directory(self):
        return self['launchingDirectory']

    @property
    def log_directory(self):
        with self.fixed_stats():
            path = os.path.dirname(self.stdout_file)
            if path:
                return path
            else:
                return self.working_directory

    @property
    def log_base(self):
        with self.fixed_stats():
            base = os.path.basename(self.stdout_file)
            base = base.split('.')
            if base[-1] == 'stdout':
                base.pop()
            name = self.name
            base = ['%jobname%' if s == name else s
                    for s in base if s]
            name = str(self.jobid)
            base = ['%jobid%' if s == name else s
                    for s in base]
            return '.'.join(base)

    @property
    def resource(self):
        with self.fixed_stats():
            cmd = self['initial_request']
            if cmd:
                properties = None
            else:
                cmd = self['wanted_resources']
                properties = self['properties']
            return oarresource.Resource.from_cli(cmd, properties)

    def __str__(self):
        try:
            with self.fixed_stats():
                stats = self.stats
                lst = []
                for key in ['name', 'project', 'state', 'owner']:
                    lst.append('{} = {}'.format(key, stats[key]))
                lst.append('runtime = {}'.format(self.runtime))
                return 'Job({})\n '.format(self.jobid) + '\n '.join(lst)
        except RuntimeError:
            return 'Job(non existing {})'.format(self.jobid)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.jobid)

    def resume(self):
        """Resume suspended job or schedule job for execution
        """
        out, err, code = oarshell.jobresume(self.jobid)
        self._raise_if_error(err, code, 'Cannot resume job')

    def suspend(self):
        """Remove job from schedule or suspend running job
        (currently not permitted)
        """
        out, err, code = oarshell.jobhold(self.jobid)
        self._raise_if_error(err, code, 'Cannot suspend job')

    def interrupt(self):
        """Stop a running, waiting or holding job
        """
        out, err, code = oarshell.jobdel(self.jobid)
        self._raise_if_error(err, code, 'Cannot suspend job')

    stop = interrupt

    @property
    def definition(self):
        with self.fixed_stats():
            kwargs = {}
            kwargs['command'] = self.command
            kwargs['name'] = self.name
            kwargs['project'] = self.project
            kwargs['working_directory'] = self.working_directory
            if self.log_directory != self.working_directory:
                kwargs['log_directory'] = self.log_directory
            kwargs['log_base'] = self.log_base
            kwargs['resource'] = self.resource
            return JobFactory(**kwargs)

    @staticmethod
    def _parse_stats(stats):
        # Dates are in local timezone
        for timekey in ['startTime', 'stopTime', 'scheduledStart', 'submissionTime']:
            value = stats.get(timekey, 0)
            if value:
                stats[timekey] = timeutils.fromtimestamp(value)
            else:
                stats[timekey] = value

        value = stats.get('walltime', None)
        if value:
            stats['walltime'] = datetime.timedelta(seconds=int(value))

    def _time_diff(self, end, start):
        """
        
        :param end: None (now)
        :type end: str or datetime or None
        :param start: None (now)
        :type start: str or datetime or None
        :return timedelta: 
        """
        with self.fixed_stats():
            return self._get_time(end) - self._get_time(start)

    def _get_time(self, tm):
        """
        
        :param tm: None (now)
        :type tm: str or datetime or None
        :return datetime: 
        """
        if isinstance(tm, datetime.datetime):
            return tm
        else:
            tm = self[tm]
            if not tm:
                tm = timeutils.now()
            return tm

    def _raise_if_error(self, err, code, msg):
        if code:
            errname = errno.errorcode.get(code, None)
            msg = '{} (Jobid={},Error={},{})\n{}'.format(msg, self.jobid, code, errname, err)
            logger.error(msg)
            raise RuntimeError(msg)

    def __eq__(self, other):
        return self.jobid == other.jobid

    def __ne__(self, other):
        return self.jobid != other.jobid

    def __lt__(self, other):
        return self.jobid < other.jobid

    def __gt__(self, other):
        return self.jobid > other.jobid

    def __le__(self, other):
        return self.jobid <= other.jobid

    def __ge__(self, other):
        return self.jobid >= other.jobid


class JobFactory(object):
    """Define and submit new jobs
    """

    def __init__(self, command=None, resource=None, name=None, project=None,
                 working_directory=None, log_directory=None, log_base=None, **resource_parameters):
        self._name = None
        self._log_base = None
        self.command = command
        if resource_parameters:
            if resource:
                logger.warning('Skip resource parameters {}'.format(resource_parameters))
            else:
                resource = oarresource.Resource(**resource_parameters)
        self.resource = resource
        self.name = name
        self.project = project
        self.working_directory = working_directory
        self.log_directory = log_directory
        self.log_base = log_base

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._default_name()

    @property
    def log_base(self):
        return self._log_base

    @log_base.setter
    def log_base(self, value):
        if value:
            self._log_base = value
        else:
            self._log_base = '%jobname%.%jobid%'
        self._default_name()

    def _default_name(self):
        if not self.name and self.log_base:
            if '%jobname%' in self.log_base:
                self.name = 'OAR'

    @property
    def cli_arguments(self):
        args = []
        if self.name:
            args += ['-n', self.name]
        if self.project:
            args += ['--project', self.project]
        if self.working_directory:
            path = os.path.expanduser(self.working_directory)
            args += ['-d', path]
        log_base = self.log_base
        if self.log_directory:
            path = os.path.expanduser(self.log_directory)
            log_base = os.path.join(path, log_base)
        args += ['-O', log_base + '.stdout']
        args += ['-E', log_base + '.stderr']
        if self.resource:
            add = self.resource.cli_arguments
            if add:
                args += add
        if self.command:
            args.append(self.command)
        return args

    @property
    def cli_string(self):
        return oarshell.cli_args2str(*self.cli_arguments)

    def __eq__(self, other):
        return self.cli_arguments == other.cli_arguments

    def __ne__(self, other):
        return self.cli_arguments != other.cli_arguments

    def __str__(self):
        return self.cli_string

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return bool(self.cli_arguments)

    def submit(self, hold=False):
        if not self.command:
            msg = 'Cannot submit a job without a command'
            logger.error(msg)
            raise RuntimeError(msg)

        cli_args = self.cli_arguments
        if hold:
            cli_args.insert(0, '--hold')
        jobid, err, code = oarshell.oarsub(*cli_args)
        if code:
            errname = errno.errorcode.get(code, None)
            msg = 'Cannot submit job (Error={}:{})\n{}'.format(code, errname, err)
            logger.error(msg)
            raise RuntimeError(msg)
        return Job(jobid)


def submit(hold=False, **parameters):
    jobdef = JobFactory(**parameters)
    return jobdef.submit(hold=hold)


def search(name=None, project=None, owner=None, state=None,
           start=None, end=None, **properties):
    """

    :param str name: 
    :param str project: 
    :param str owner: 
    :param datetime start: 
    :param datetime end: 
    :param str state: 
    :return list: list of jobs
    """
    # https://github.com/oar-team/oar/blob/2.5/sources/core/database/mysql_structure.sql
    sqlquery = []
    if name:
        sqlquery.append("job_name='{}'".format(name))
    if project:
        sqlquery.append("project='{}'".format(project))
    if owner:
        sqlquery.append("job_user='{}'".format(owner))
    if state:
        sqlquery.append("state='{}'".format(state))
    if start:
        start = timeutils.totimestamp(start)
        sqlquery.append("start_time>='{}'".format(start))
    if end:
        end = timeutils.totimestamp(end)
        sqlquery.append("stop_time<='{}'".format(end))
    for k, (op, v) in properties.items():
        sqlquery.append("{}{}'{}'".format(k, op, v))
    if not sqlquery:
        return []

    result, err, code = oarshell.oarstat('--sql', ' and '.join(sqlquery))
    if code:
        # json parsing gives error when query returns no results
        # (bug in OAR perl library) so don't raise an exception here
        errname = errno.errorcode.get(code, None)
        msg = 'Job search error {} ({})\n{}'.format(code, errname, err)
        logger.debug(msg)
        # raise RuntimeError(msg)
        return []
    if result:
        return [Job(jobid) for jobid in result]
    else:
        return []
