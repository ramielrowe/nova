# Copyright (c) 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Image Count Weigher.  Weigh hosts by their active Images.

"""

from oslo.config import cfg

from nova.scheduler import weights

ram_weight_opts = [
        cfg.FloatOpt('image_count_weight_multiplier',
                     default=1.0,
                     help='Multiplier used for weighing image_count. '
                          'Positive values cause builds to prefer hosts '
                          'with image already present. Negative values '
                          'cause builds to prefer hosts without image '
                          'already present.'),
        cfg.BoolOpt('image_count_weight_inverse_growth',
                    default=True,
                    help='Inverses the impact of image count on host weight. '
                         'Hosts with a given image will still be preferred '
                         'but instead of stacking, instances will be spread '
                         'between hosts with a given image.')
]

CONF = cfg.CONF
CONF.register_opts(ram_weight_opts)


class ImageCountWeigher(weights.BaseHostWeigher):
    def weight_multiplier(self):
        """Override the weight multiplier."""
        return CONF.image_count_weight_multiplier

    def _weigh_object(self, host_state, weight_properties):
        """Higher weights win.  We want spreading to be the default."""
        stat_key = 'num_img_%s' % weight_properties['image_ref']
        count = float(host_state.stats.get(stat_key, 0))
        if count and CONF.image_count_weight_inverse_growth:
            count = 1.0/count
        return count