# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    invoice_policy = fields.Selection(
        selection_add=[
            ('threshold', 'Invoice and Enforce a Threshold'),
            ('usage', 'Invoice Based on Usage'),
        ],
    )
