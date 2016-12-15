# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderConfigCertificateAbstract(models.AbstractModel):
    """ It provides data handling for certificate client + server configs. """

    _name = 'clouder.config.certificate.abstract'
    _description = 'Clouder Config Certificate Abstract'

    sign_policy_default_id = fields.Many2one(
        string='Default Signing Policy',
        comodel_name='clouder.certificate.policy.sign',
        required=True,
    )
    sign_policy_profile_ids = fields.Many2many(
        string='Signing Policy Profiles',
        comodel_name='clouder.certificate.policy.sign',
    )
    auth_policy_ids = fields.Many2many(
        string='Auth Policies',
        comodel_name='clouder.certificate.policy.auth',
        compute='_compute_auth_policy_ids',
    )
    computed = fields.Serialized(
        compute="_compute_computed",
    )

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request. """
        for record in self:
            profiles = {
                p.name: p.computed for p in record.sign_policy_profile_ids
            }
            auth_keys = {
                auth.name: auth.computed for auth in record.auth_policy_ids
            }
            record.computed_config = {
                'signing': {
                    'default': record.sign_policy_default_id.computed,
                    'profiles': profiles,
                },
                'auth_keys': auth_keys,
            }

    @api.multi
    def to_json(self):
        """ It returns the JSON representation of this object """
        self.ensure_one()
        return json.dumps(self.computed)
