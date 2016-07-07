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

class OstroLaunchError(Exception):
    pass

def clone_zephyr(url, dest):
    cmd = "git clone {} {}".format(url, dest).split()

    try:
        print "Attempting to clone {}".format(url)
        subprocess.check_call(cmd, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError:
        errormsg = 'Unable to clone "{}".'.format(args.url)
        raise OstroLaunchError(errormsg)

parser = argparse.ArgumentParser()

parser.add_argument("--git", help="git repo with zephyr kernel source")
parser.add_argument("--workdir", default='/workdir',
                    help="Directory containing the zephyr kernel source. "
                         "Or the location to prepare the git repo"
                         "if --git was specfied.")

args = parser.parse_args()

try:
    if not os.path.exists(args.workdir):
        os.mkdir(args.workdir)

    zephyrfound = os.path.exists(os.path.join(args.workdir,".git"))

    if zephyrfound and args.git:
        errormsg = ('A git repository was found in {} yet "--git" was also '
                    'specified. Cowardly refusing to overwrite existing repo.')
        errormsg = errormsg.format(args.workdir)
        print(errormsg)

    elif not zephyrfound and not args.git:
        errormsg = ('A zephyr git repository was not found in {}. "--git"'
                    'must be specified.')
        errormsg = errormsg.format(args.workdir)
        raise OstroLaunchError(errormsg)

    elif not zephyrfound and args.git:
        clone_zephyr(args.git, args.workdir)

    # Source the environment setup script and run bash
    cmd = 'bash -c'.split()
    args = 'cd {}; exec bash -i'.format(args.workdir)
    os.environ["LC_CTYPE"] = "en_US.UTF-8"
    os.execvp(cmd[0], cmd + [args])

except OstroLaunchError as e:
    print e
