# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json

from odoo import api, fields, models


class ClouderCertificateAuthority(models.Model):
    """ It provides an interface for controlling a Cert Authority. """

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
    exec_service_id = fields.Many2one(
        string='Executor Service',
        comodel_name='clouder.service',
        compute='_compute_exec_service_id',
    )
    config_id = fields.Many2one(
        string='Configuration',
        comodel_name='clouder.config.certificate.server',
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
