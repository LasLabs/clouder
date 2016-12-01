# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ClouderMetricInterface(models.Model):
    """ It provides a common interface for Clouder Usage metrics """

    _name = 'clouder.metric.interface'
    _inherits = {'clouder.metric.type': 'type_id'}

    service_id = fields.Many2one(
        string='Service',
        comodel_name='clouder.service',
        required=True,
    )
    type_id = fields.Many2one(
        string='Metric Trype',
        comodel_name='clouder.metric.type',
        required=True,
        ondelete='restrict',
    )
    metric_ids = fields.One2many(
        string='Metric Values',
        comodel_name='clouder.metric.value',
        inverse_name='interface_id',
    )
