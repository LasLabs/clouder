# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json

from odoo import api, fields, models


class ClouderCertificateAuthority(models.Model):
    """ It provides an interface for controlling a Cert Authority """

    _name = 'clouder.certificate.authority'
    _description = 'Clouder Certificate Authority'
    _inherits = {'clouder.application': 'application_id'}

    application_id = fields.Many2one(
        string='Application',
        comodel_name='clouder.application',
        required=True,
        ondelete='cascade',
        domain=lambda s: "[('tag_ids', '=', %d)]" % s.enf.ref(
            'clouder_certificate_authority.tag_cert_authority',
        ),
    )
    private_key_id = fields.Many2one(
        string='Private Key',
        comodel_name='clouder.key.private',
        domain="[('is_private', '=', True)]",
        context="{'default_is_private': True}",
    )
    certificate_id = fields.Many2one(
        string='Certificate',
        comodel_name='clouder.key.public',
        related='certificate_request_id.public_key_id',
    )
    certificate_request_id = fields.Many2one(
        string='CSR',
        comodel_name='clouder.certificate.request',
    )
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
    exec_service_id = fields.Many2one(
        string='Executor Service',
        comodel_name='clouder.service',
        compute='_compute_exec_service_id',
    )
    computed_config = fields.Serialized(
        compute="_compute_computed_config",
    )

    @api.multi
    def _compute_auth_policy_ids(self):
        for record in self:
            policies = sum((record.sign_policy_default_id,
                            record.sign_policy_profile_ids,
                            ))
            record.auth_policy_ids = policies.mapped('auth_policy_id')

    @api.multi
    def _compute_exec_service_id(self):
        for record in self:
            service_ids = record.service_ids.filtered(
                lambda s: s.code == 'exec',
            )
            record.exec_service_id = service_ids[0]

    @api.multi
    def _compute_computed_config(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            profiles = {
                p.name: p.computed for p in record.sign_policy_profile_ids
            }
            auth_keys = {
                auth.name: auth.computed for auth in record.auth_policy_ids
            }
            record.computed_config = {
                'signing': record.sign_policy_default_id.computed,
                'profiles': profiles,
                'auth_keys': auth_keys,
            }

    @api.multi
    def get_json(self, computed_type='config'):
        """ It returns the JSON representation of this object """
        self.ensure_one()
        attribute = get(self, 'computed_%s' % computed_type)
        return json.dumps(attribute)
