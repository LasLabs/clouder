# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ClouderContractLine(models.Model):
    """ It provides the link between billing and Clouder Services. """

    _name = 'clouder.contract.line'
    _inherits = {'account.analytic.invoice.line': 'contract_line_id'}

    contract_line_id = fields.Many2one(
        string='Recurring Line',
        comodel_name='account.analytic.invoice.line',
        index=True,
        required=True,
        ondelete='restrict',
    )
    service_id = fields.Many2one(
        string='Clouder Service',
        comodel_name='clouder.service',
        related='metric_interface_id.service_id',
        required=True,
    )
    metric_interface_id = fields.Many2one(
        string='Metric Interface',
        comodel_name='clouder.metric.interface',
        required=True,
    )
