# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ClouderMetricType(models.Model):
    """ It provides context for usage metric types """

    _name = 'clouder.metric.type'

    name = fields.Char()
    code = fields.Char()
    uom_id = fields.Many2one(
        string='Unit of Measure',
        comodel_name='product.uom',
    )
