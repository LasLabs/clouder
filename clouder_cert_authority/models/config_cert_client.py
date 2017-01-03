# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from ..api import API


class ClouderConfigCertClient(models.Model, API):
    """ It provides data handling for cert client configs. """

    _name = 'clouder.config.cert.client'
    _inherit = 'clouder.config.cert.abstract'
    _description = 'Clouder Config Cert Client'

    remote_ids = fields.Many2many(
        string='Remotes',
        comodel_name='clouder.cert.host',
        required=True,
    )

    @api.multi
    def _compute_api_object(self):
        """ It computes the keys required for the JSON request. """
        for record in self:
            super(ClouderConfigCertClient, record)._compute_api_object()
            remotes = {
                remote.name: remote.api_object for remote in record.remote_ids
            }
            record.api_object = self.cfssl.ConfigClient(
                sign_policy_default=record.api_object.sign_policy,
                sign_policies_add=record.api_object.sign_policies,
                auth_policies=record.api_object.auth_policies,
                remotes=remotes,
            )
