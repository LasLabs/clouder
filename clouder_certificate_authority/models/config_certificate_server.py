# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models

from ..api import API


class ClouderConfigCertificateServer(models.Model, API):
    """ It provides data handling for certificate server configs. """

    _name = 'clouder.config.certificate.server'
    _inherit = 'clouder.config.certificate.abstract'
    _description = 'Clouder Config Certificate Server'

    @api.multi
    def _compute_api_object(self):
        """ It computes the keys required for the JSON request. """
        for record in self:
            super(ClouderConfigCertificateServer, record)._compute_api_object()
            record.api_object = self.cfssl.ConfigServer(
                sign_policy_default=record.api_object.sign_policy,
                sign_policies_add=record.api_object.sign_policies,
                auth_policies=record.api_object.auth_policies,
            )
