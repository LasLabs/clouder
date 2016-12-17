# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from ..api import API


class ClouderConfigCertificateAbstract(models.AbstractModel, API):
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
    api_object = fields.Binary(
        compute="_compute_api_object",
    )

    @api.multi
    def _compute_api_object(self):
        """ It computes the keys required for the JSON request. """
        for record in self:
            profiles = record.sign_policy_profile_ids.mapped('api_object')
            auth_keys = record.auth_policy_ids.mapped('api_object')
            record.api_object = self.cfssl.ConfigMixer(
                sign_policy=record.sign_policy_default_id.api_object,
                sign_policies=profiles,
                auth_policies=auth_keys,
            )
