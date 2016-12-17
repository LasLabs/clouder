# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from ..api import API


class ClouderCertificateX509(models.Model, API):
    """ It provides the concept of a signed certificate. """

    _name = 'clouder.certificate.x509'
    _inherit = 'clouder.certificate.abstract'
    _description = 'Clouder Certificate X.509'

    subject_key = fields.Char(
        required=True,
        help='X509v3 Subject Key Identifier.',
    )
    authority_key = fields.Char(
        required=True,
        help='X509v3 Authority Key Identifier.',
    )
    public_key_id = fields.Many2one(
        string='Public Key',
        comodel_name='clouder.key.public',
        required=True,
        context="{'default_request_id': request_id}",
    )
    request_id = fields.Many2one(
        string='CSR',
        comodel_name='clouder.certificate.request',
        required=True,
    )
    use_policy_ids = fields.Many2many(
        string='Use Policies',
        comodel_name='clouder.certificate.policy.use',
    )
