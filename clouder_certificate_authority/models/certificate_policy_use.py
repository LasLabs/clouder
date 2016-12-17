# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderCertificatePolicyUse(models.Model):
    """ It provides a CA Signature Use Policy """

    _name = 'clouder.certificate.policy.use'
    _description = 'Clouder Certificate Usage Policy'
    _order = 'sequence, name'

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    sequence = fields.Integer(
        required=True,
        default=5,
    )
    api_object = fields.Binary(
        compute="_compute_api_object",
    )

    _sql_constraints = [
        ('code_uniq', 'UNIQUE(code)', 'Code must be unique.'),
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique.'),
    ]

    @api.multi
    def _compute_api_object(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.api_object = self.cfssl.PolicyUse(
                name=record.name,
                code=record.code,
            )
