# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ClouderMetricValue(models.Model):
    """ It provides a record of metric values used in billin """

    _name = 'clouder.metric.value'

    interface_id = fields.Many2one(
        string='Interface',
        comodel_name='clouder.metric.interface',
        required=True,
    )
    value = fields.Float(
        required=True,
    )
    uom_id = fields.Many2one(
        string='Unit of Measure',
        comodel_name='product.uom',
        related='interface_id.uom_id',
    )
