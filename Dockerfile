# Copyright (C) 2015-2016 Intel Corporation
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

#
# zephyr build container
#

FROM crops/yocto:ubuntu-16.04-base

USER root
ENV ZEPHYR_GCC_VARIANT zephyr
ENV ZEPHYR_SDK_INSTALL_DIR /opt/zephyr-sdk

ARG ZEPHYR_SRC

ADD https://raw.githubusercontent.com/crops/extsdk-container/master/restrict_useradd.sh  \
    https://raw.githubusercontent.com/crops/extsdk-container/master/restrict_groupadd.sh \
    https://raw.githubusercontent.com/crops/extsdk-container/master/usersetup.py \
    /usr/bin/
ADD ${ZEPHYR_SRC} /tmp

COPY zephyr-launch.py \
     zephyr-entry.py \
     /usr/bin/

COPY sudoers.usersetup /etc/

# We remove the user because we add a new one of our own.
# The usersetup user is solely for adding a new user that has the same uid,
# as the workspace. 70 is an arbitrary *low* unused uid on debian.
RUN userdel -r yoctouser && \
    groupadd -g 70 usersetup && \
    useradd -N -m -u 70 -g 70 usersetup && \
    apt-get update -y && \
    apt-get -y install sudo libncurses5-dev && \
    echo "#include /etc/sudoers.usersetup" >> /etc/sudoers && \
    chmod 755 /usr/bin/usersetup.py \
              /usr/bin/zephyr-launch.py \
              /usr/bin/zephyr-entry.py \
              /usr/bin/restrict_groupadd.sh \
              /usr/bin/restrict_useradd.sh \
              /tmp/zephyr-sdk* && \
   /tmp/zephyr-sdk* -- -y -d /opt/zephyr-sdk/

USER usersetup

ENTRYPOINT ["zephyr-entry.py"]
