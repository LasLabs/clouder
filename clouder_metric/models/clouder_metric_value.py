# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ClouderMetricValue(models.Model):
    """ It provides a record of metric values used in billing. """

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
    )
    date_start = fields.Datetime(
        string='Metric Start',
    )
    date_end = fields.Datetime(
        string='Metric End',
    )
    date_create = fields.Datetime(
        string='Creation Time',
        default=lambda s: fields.Datetime.now(),
    )
