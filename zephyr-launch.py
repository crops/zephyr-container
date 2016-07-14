#!/usr/bin/env python

# zephyr-launch.py
#
# Copyright (C) 2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import argparse
import os
import sys
import subprocess
import shlex

class OstroLaunchError(Exception):
    pass

def clone_zephyr(url, dest):
    cmd = "git clone {}".format(url)
    cmd = shlex.shlex(cmd, posix=True)
    cmd.whitespace_split = True
    cmd = list(cmd)
    try:
        print "Attempting to clone {}".format(url)
        subprocess.check_call(cmd, cwd=dest, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError:
        errormsg = 'Unable to clone "{}".'.format(url)
        raise OstroLaunchError(errormsg)

parser = argparse.ArgumentParser()

parser.add_argument("--git", nargs='+', help="git repo with zephyr kernel source")
parser.add_argument("--workdir", default='/workdir',
                    help="Directory containing the zephyr kernel source. "
                         "Or the location to prepare the git repo"
                         "if --git was specfied.")

args = parser.parse_args()
if args.git is not None:
    args.git = (','.join(args.git)).replace(":|", " ")

try:
    if not os.path.exists(args.workdir):
        os.mkdir(args.workdir)

    zephyrfound = os.path.exists(os.path.join(args.workdir,"zephyr"))

    if not zephyrfound and args.git is None:
        errormsg = ('You need to check out a zephyr kernel to build zephyr apps, e.g. git clone https://gerrit.zephyrproject.org/r/zephyr')
        print(errormsg)

    elif args.git is not None:
        clone_zephyr(args.git, args.workdir)

    cmd = 'bash -c'.split()
    args = 'cd {}; exec bash -i'.format(args.workdir)
    os.execvp(cmd[0], cmd + [args])

except OstroLaunchError as e:
    print e
