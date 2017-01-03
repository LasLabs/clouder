# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from ..api import API


class ClouderCertHost(models.Model, API):
    """ It provides the concept of a cert's CommonName """

    _name = 'clouder.cert.host'
    _description = 'Clouder Cert Host'

    name = fields.Char(
        required=True,
    )
    host = fields.Char(
        required=True,
    )
    port = fields.Integer()
    api_object = fields.Binary(
        compute="_compute_api_object",
    )

    @api.multi
    def _compute_api_object(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.api_object = self.cfssl.Host(
                name=record.name,
                host=record.host,
                port=record.port,
            )
