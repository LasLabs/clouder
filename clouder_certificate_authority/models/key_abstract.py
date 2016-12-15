# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderKeyAbstract(models.AbstractModel):
    """ It provides attributes and methods related to all keys """

    _name = 'clouder.key.public'
    _description = 'Clouder Key Public'

    name = fields.Char(
        required=True,
    )
    description = fields.Char()
    mime_type = fields.Selection(
        selection='_get_mime_types',
    )
    attachment_id = fields.Many2one(
        string='Key',
        comodel_name='ir.attachment',
        required=True,
        context="""{
            'default_type': 'binary',
            'default_res_model': _name,
            'default_res_field': 'attachment_id',
            'default_res_id': id,
            'default_name': name,
            'default_description': description,
            'default_mime_type': mime_type,
        }""",
    )
    data = fields.Text(
        related='attachment_id.datas',
    )

    @api.model
    def _get_mime_types(self):
        return [
            ('application/pkcs8', 'PKCS-8'),
            ('application/pkcs10', 'PKCS-10'),
            ('application/x-pkcs12', 'PKCS-12'),
            ('application/x-pem-file', 'PEM'),
            ('application/pkcs7-mime', 'PKCS-7 MIME'),
            ('application/x-x509-ca-cert', 'X.509 CA'),
            ('application/x-x509-user-cert', 'X.509 User'),
        ]
