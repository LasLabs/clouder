# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderKeyPrivate(models.Model):
    """ It provides the concept of a Private Key """

    _name = 'clouder.key.private'
    _inherit = 'clouder.key.abstract'
    _description = 'Clouder Key Private'

    public_key_id = fields.Many2one(
        string='Public Key',
        comodel_name='clouder.key.public',
    )

    @api.model
    def create(self, vals):
        vals['is_private'] = True
        return super(ClouderKeyPrivate, self).create(vals)
