# Copyright (c) 2014 Rackspace Hosting
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
In order to increase the likelihood of a cache hit, weight cells higher
if they already have active instances with current instance's image.
"""

from oslo.config import cfg
from oslo.utils import timeutils

from nova.cells import weights
from nova import db
from nova.i18n import _LW
from nova.openstack.common import log as logging

LOG = logging.getLogger(__name__)

image_weigher_opts = [
        cfg.FloatOpt('image_weight_multiplier',
                default=10.0,
                help='Multiplier used to weigh image_count. (The value '
                     'should be positive.)'),
        cfg.BoolOpt('image_weight_inverse_growth',
                    default=True,
                    help='Inverses the impact of image count on cell weight. '
                         'Cells with a given image will still be preferred '
                         'but instead of stacking, instances will be spread '
                         'between cells with a given image.')
]

CONF = cfg.CONF
CONF.register_opts(image_weigher_opts, group='cells')


class ImageByInstanceCountWeigher(weights.BaseCellWeigher):
    """If a child has active instances with current instance's image
    weigh them higher.
    """

    def weight_multiplier(self):
        # positive multiplier => height weight
        return CONF.cells.image_weight_multiplier

    def inverse_growth(self):
        return CONF.cells.image_weight_inverse_growth

    def _weigh_object(self, cell, weight_properties):
        pass

    def _weigh_cell(self, cell, image_counts):
        cell_name = cell.obj.name
        weight = 0
        if cell_name in image_counts and image_counts[cell_name]:
            count = image_counts[cell_name]
            weight = 1 / count if self.inverse_growth() else count
        return weight

    def weigh_objects(self, cells, weight_properties):
        context = weight_properties['context']
        weights = []

        inst_props = weight_properties['request_spec']['instance_properties']
        image_ref = inst_props['image_ref']
        image_counts = db.cell_get_instance_count_by_image(context, image_ref)

        for cell in cells:
            weight = self._weigh_cell(cell, image_counts)
            weights.append(weight * self.weight_multiplier())

        return weights
