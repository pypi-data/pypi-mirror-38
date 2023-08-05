#!/usr/bin/env python
"""
Copyright (c) 2018 Guanzhong Chen.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import print_function

import argparse
import gzip
import os
import shlex
import subprocess
import sys
import time
from functools import partial

BUFSIZE = 4096
timer = getattr(time, 'monotonic', [time.time, time.clock][os.name == 'nt'])


def main():
    parser = argparse.ArgumentParser(description='Runs a command, and sends its output to a Jenkins external job.')
    parser.add_argument('host', help='Jenkins hostname (for Jenkins SSH server)')
    parser.add_argument('port', help='Jenkins SSH server port', type=int)
    parser.add_argument('job', help='Jenkins job name')
    parser.add_argument('command', help='command to be run under this script')
    parser.add_argument('args', help='arguments to pass to the command', nargs='*')
    parser.add_argument('-u', '--user', help='Jenkins user to login as (using public key authentication, '
                                             'default: your username)')
    parser.add_argument('-d', '--display-name', help='display name of the build')
    parser.add_argument('-s', '--ssh-command', help='ssh command', default='ssh')
    parser.add_argument('-x', '--executable', help='the executable to actually use')
    parser.add_argument('-q', '--no-job-id', help='do not print the job ID in the end', action='store_true')

    args = parser.parse_args()

    start_time = timer()
    process = subprocess.Popen([args.command] + args.args, executable=args.executable,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if sys.stdout.isatty():
        read_func = process.stdout.readline
    else:
        read_func = partial(process.stdout.read, BUFSIZE)

    if sys.version_info[0] >= 3:
        stdout = sys.stdout.buffer
    else:
        stdout = sys.stdout

    pieces = []
    for piece in iter(read_func, b''):
        pieces.append(piece)
        stdout.write(piece)

    exit_code = process.wait()
    duration = timer() - start_time

    host = '%s@%s' % (args.user, args.host) if args.user else args.host
    ssh_command = shlex.split(args.ssh_command) + ['-p%d' % (args.port,), host, 'set-external-build-result']
    ssh_command += ['--job', args.job, '--result', str(exit_code), '--duration', str(int(duration * 1000))]
    ssh_command += ['--log', '-', '-b']
    if args.display_name:
        ssh_command += ['--display', args.display_name]
    ssh = subprocess.Popen(ssh_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    with ssh.stdin, gzip.GzipFile(fileobj=ssh.stdin) as f:
        for piece in pieces:
            f.write(piece)
        f.write(b'\nJob finished in %.3f seconds with exit code %d.\n' % (duration, exit_code))

    job_id = ssh.stdout.read()
    try:
        job_id = int(job_id)
    except ValueError:
        print('Got invalid job ID from Jenkins:', job_id, file=sys.stderr)

    if not args.no_job_id:
        print('Logged as job %d on %s.' % (job_id, args.job), file=sys.stderr)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
