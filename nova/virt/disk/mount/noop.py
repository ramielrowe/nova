# Copyright 2014 Rackspace Hosting, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""No operation mounter for LVM based images."""

from nova.virt.disk.mount import api


class NoopMount(api.Mount):
    """LVM images are already mounted, thus don't need further mounting."""
    mode = 'noop'

    def _inner_get_dev(self):
        self.device = self.mount_dir
        self.mounted = True
        return True

    def get_dev(self):
        # NOTE(mikal): the retry is required here in case we are low on loop
        # devices. Note however that modern kernels will use more loop devices
        # if they exist. If you're seeing lots of retries, consider adding
        # more devices.
        return self._get_dev_retry_helper()

    def unget_dev(self):
        if not self.mounted:
            return

        self.mounted = False
        self.device = None
