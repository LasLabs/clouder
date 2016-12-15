# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderCertificate(models.Model):
    """ It provides the concept of a Certificate """

    _name = 'clouder.certificate.request'
    _description = 'Clouder Certificate Request'

    authority_id = fields.Many2one(
        string='Cert Authority',
        comodel_name='clouder.certificate.authority',
        required=True,
        ondelete='cascade',
    )
    common_name_id = fields.Many2one(
        string='Common Name',
        comodel_name='clouder.certificate.host',
        required=True,
    )
    subject_info_ids = fields.Many2many(
        string='Names',
        comodel_name='clouder.certificate.name',
        required=True,
    )
    computed = fields.Serialized(
        compute="_compute_computed",
    )

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.computed = {
                'CN': record.common_name_id.name,
                'names': [
                    name.computed for name in record.subject_info_ids
                ],
            }
