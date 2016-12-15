# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from odoo.addons.clouder.tools import generate_random_password


class ClouderCertificatePolicyAuth(models.Model):
    """ It provides a CA Signature Auth Policy """

    _name = 'clouder.certificate.policy.auth'
    _description = 'Clouder Certificate Auth Policy'

    name = fields.Char(
        required=True,
    )
    key = fields.Char(
        required=True,
        default=lambda s: s._default_key(),
    )
    key_type = fields.Selection([
        ('standard', 'Standard'),
    ],
        default='standard',
        required=True,
    )
    computed = fields.Serialized(
        compute="_compute_computed",
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique.'),
        ('key_uniq', 'UNIQUE(key)', 'Key must be unique.'),
    ]

    @api.model
    def _default_key(self):
        passwd = generate_random_password()
        return passwd.encode('hex')[:16]

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.computed = {
                'key': record.key,
                'type': record.key_type,
            }
