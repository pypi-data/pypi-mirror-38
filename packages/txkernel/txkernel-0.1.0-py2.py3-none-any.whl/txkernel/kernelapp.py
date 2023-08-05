# txkernel
# Copyright (C) 2018  guysv

# This file is part of txkernel which is released under GPLv2.
# See file LICENSE or go to https://www.gnu.org/licenses/gpl-2.0.txt
# for full license details.

"""
This module implements a kernel entry-point.

The typical Jupyter kernel has two app modes:

child mode: The kernel is launched as a child
process of a Jupyter frontend, and its connection
file is made by the frontend.

passive mode: The kernel is launched as a
stand-alone program, and generates its connection
file by itself. The connection file path is then
returned to the user for frontend connections.
"""
import sys
import argparse
import os
from os import path
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import zmq
from twisted.internet import task
from twisted.logger import globalLogBeginner, FilteringLogObserver, \
                           textFileLogObserver, LogLevel, PredicateResult
from .connection import ConnectionFile

class KernelApp(object):
    _NAME_TO_LEVEL = {
        'debug': LogLevel.debug,
        'info': LogLevel.info,
        'warn': LogLevel.warn,
        'error': LogLevel.error,
        'critical': LogLevel.critical
    }

    ENV_VAR_PREFIX = "TXKERNEL_"

    def __init__(self, kernel_cls, *extra_kernel_args, **extra_kernel_kwargs):
        self.kernel_cls = kernel_cls
        self.extra_kernel_args = extra_kernel_args
        self.extra_kernel_kwargs = extra_kernel_kwargs

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-l', '--log-level',
                                 default=self._get_default('LOG_LEVEL',
                                                           'warn'),
                                 metavar="LEVEL",
                                 choices=self._NAME_TO_LEVEL.keys(),
                                 help="Show only certain logs")
    
    def run(self):
        # separated from other options to give subclasses a chance to override
        self.parser.add_argument('-c', '--connection-file',
                            help="Path to existing connection file")
        cli_args = vars(self.parser.parse_args())
        
        # wow twisted log api sucks bigtime
        # all this mess just to set global log level
        filter_level = self._NAME_TO_LEVEL[cli_args.pop("log_level")]
        log_filter =\
            lambda e: PredicateResult.yes if e['log_level'] >= filter_level\
                      else PredicateResult.no
        observer = FilteringLogObserver(textFileLogObserver(sys.stdout),
                                        [log_filter])
        globalLogBeginner.beginLoggingTo([observer], redirectStandardIO=False)

        if cli_args.get("connection_file"):
            connection_file =\
                ConnectionFile.from_existing(cli_args.pop("connection_file"))
            write_connection_file = False
        else:
            connection_file = ConnectionFile.generate()
            write_connection_file = True
        
        self.extra_kernel_kwargs.update(cli_args)

        self.kernel = self.kernel_cls(connection_file.connection_props,
                                      *self.extra_kernel_args,
                                      **self.extra_kernel_kwargs)

        if write_connection_file:
            # Fix socket ports
            props = connection_file.connection_props
            props["shell_port"] = self._get_socket_port(self.kernel.shell_sock)
            props["control_port"] = self._get_socket_port(self.kernel.ctrl_sock)
            props["iopub_port"] = self._get_socket_port(self.kernel.iopub_sock)
            props["stdin_port"] = self._get_socket_port(self.kernel.stdin_sock)
            props["hb_port"] = self._get_socket_port(self.kernel.hb_sock)

            connection_file_path = connection_file.write_file()
            hint = """To connect another client to this kernel, use:
        --existing {}""".format(path.basename(connection_file_path))
            print(hint)
        
        return task.react(lambda r: self.kernel.run())
    
    def _get_default(self, env_var_name, default):
        return os.environ.get(self.ENV_VAR_PREFIX + env_var_name, default)

    @staticmethod
    def _get_socket_port(socket):
        # pylint: disable=maybe-no-member
        return urlparse(socket.socket.getsockopt(zmq.LAST_ENDPOINT)).port
