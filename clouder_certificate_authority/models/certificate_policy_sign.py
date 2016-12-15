# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderCertificatePolicySign(models.Model):
    """ It provides a CA Signature Policy """

    _name = 'clouder.certificate.policy.sign'
    _description = 'Clouder Certificate Signing Policy'

    name = fields.Char(
        required=True,
    )
    usage_ids = fields.Many2many(
        string='Usages',
        comodel_name='clouder.certificate.policy.use',
        required=True,
    )
    auth_policy_id = fields.Many2one(
        string='Auth Key',
        comodel_name='clouder.certificate.policy.auth',
        required=True,
    )
    expire_hours = fields.Integer(
        required=True,
        default=(365 * 24),
    )
    computed = fields.Serialized(
        compute="_compute_computed",
    )

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.computed = {
                'auth_key': record.auth_policy_id.name,
                'expiry': '%sh' % expire_hours,
                'usages': [
                    usage.code for usage in record.usage_ids
                ],
            }
