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

import datetime
import re
from . import oarshell


def walltime2str(tdelta):
    h, rem = divmod(int(round(tdelta.total_seconds())), 3600)
    m, s = divmod(rem, 60)
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def str2walltime(s):
    h, m, s = s.split(':')
    return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))


property_pattern = re.compile('(\w+)([>=<]+)\'?([\w\d]+)\'?')


# Includes the default ones (space around operator):
# property_pattern = re.compile('(\w+) *([>=<]+) *\'?([\w\d]+)\'?')

class Resource(object):
    def __init__(self, host=None, nodes=None, cpu=None, core=None, gpu=False,
                 walltime=None, mem_core_mb=None, **properties):
        """
        
        Custom properties can be defined: for example cpu_vendor=('=',INTEL)"

        :param int host: number of nodes to be used (Optional)
        :param int nodes: number of nodes to be used (Optional)
        :param int cpu: number of cpu's per node (Optional)
        :param int core: number of cores per cpu (Optional)
        :param bool gpu: need a gpu or not (Optional)
        :param walltime: hours when a number, dict keys: days, seconds,
                         microseconds, milliseconds, minutes, hours, weeks
                         (Optional)
        :type walltime: timedelta or dict or num
        :param int mem_core_mb: required memory per core in MB (Optional)
        """
        if not nodes:
            nodes = host
        self.nodes = nodes
        self.cpu = cpu
        self.core = core
        self.gpu = gpu
        self.walltime = walltime
        self.mem_core_mb = mem_core_mb
        self.properties = properties

    @property
    def walltime(self):
        return self._walltime

    @walltime.setter
    def walltime(self, value):
        if isinstance(value, datetime.timedelta) or value is None:
            self._walltime = value
        else:
            try:
                self._walltime = datetime.timedelta(**value)
            except TypeError:
                self._walltime = datetime.timedelta(hours=value)

    @property
    def memory(self):
        return self.cores * self.mem_core_mb

    @property
    def cores(self):
        n = 1
        for m in [self.nodes, self.cpu, self.core]:
            if m:
                n *= m
        return n

    @property
    def _cli_resource(self):
        resources = []
        if self.nodes:
            resources.append('nodes={}'.format(self.nodes))
        if self.cpu:
            resources.append('cpu={}'.format(self.cpu))
        if self.core:
            resources.append('core={}'.format(self.core))
        cliarg = '/'.join(resources)
        if self.walltime:
            walltime = walltime2str(self.walltime)
            if cliarg:
                cliarg = '{},walltime={}'.format(cliarg, walltime)
            else:
                cliarg = 'walltime={}'.format(walltime)
        return cliarg

    @property
    def _cli_properties(self):
        properties = []
        if self.gpu:
            properties.append("gpu='YES'")
        if self.mem_core_mb:
            properties.append("mem_core_mb>={:d}".format(self.mem_core_mb))
        for k, (op, v) in self.properties.items():
            properties.append("{}{}'{}'".format(k, op, v))
        cliarg = ' and '.join(properties)
        return cliarg

    @property
    def cli_arguments(self):
        args = []
        add = self._cli_resource
        if add:
            args += ['-l', add]
        add = self._cli_properties
        if add:
            args += ['-p', add]
        return args

    @property
    def cli_string(self):
        return oarshell.cli_args2str(*self.cli_arguments)

    @classmethod
    def from_cli(cls, cmd, properties=None):
        kwargs = {}
        cli_arguments = list(oarshell.cli_str2args(cmd))
        arg = oarshell.cli_getarg(cli_arguments, '-l')
        if arg:
            for key in ['host', 'nodes', 'cpu', 'core']:
                match = re.search('{}=(\d+)'.format(key), arg)
                if match:
                    kwargs[key] = match.groups()[0]
            match = re.search('walltime=(\d+:\d+:\d+)', arg)
            if match:
                kwargs['walltime'] = str2walltime(match.groups()[0])
        arg = oarshell.cli_getarg(cli_arguments, '-p')
        if not arg and properties:
            arg = properties
        if arg:
            for match in property_pattern.finditer(arg):
                k, op, v = match.groups()
                if k == 'gpu':
                    kwargs['gpu'] = v == 'YES'
                elif k == 'mem_core_mb':
                    kwargs['mem_core_mb'] = int(v)
                else:
                    kwargs[k] = op, v
        return cls(**kwargs)

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
