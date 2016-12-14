# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ClouderKeyPublic(models.Model):
    """ It provides attributes and methods related to handling public keys """

    _name = 'clouder.key.public'
    _description = 'Clouder Key Public'

    name = fields.Char(
        required=True,
    )
    attachment_id = fields.Many2one(
        string='Key',
        comodel_name='ir.attachment',
        required=True,
        context="""{
            'default_type': 'binary',
            'default_res_model': 'clouder.key.public',
            'default_res_field': 'attachment_id',
            'default_res_id': id,
            'default_name': name,
        }""",
    )
    data = fields.Text(
        related='attachment_id.datas',
    )
