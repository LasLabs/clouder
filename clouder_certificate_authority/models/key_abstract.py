# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderKeyAbstract(models.Model):
    """ It provides attributes and methods related to all keys """

    _name = 'clouder.key.abstract'
    _inherit = 'clouder.certificate.abstract'
    _description = 'Clouder Key Abstract'

    strength = fields.Integer(
        default=4096,
    )
    algorithm = fields.Selection(
        default='rsa',
        selection=lambda s: s._get_algorithms(),
    )
    is_private = fields.Boolean()
    active = fields.Boolean(
        default=True,
    )

    @api.model
    def _get_algorithms(self):
        return [
            ('rsa', 'RSA'),
            ('ecdsa', 'ECDSA'),
        ]
