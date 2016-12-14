# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ClouderCertificateRequest(models.Model):
    """ It provides the concept of a Certificate Request """

    _name = 'clouder.certificate.request'
    _description = 'Clouder Certificate Request'

    authority_id = fields.Many2one(
        string='Cert Authority',
        comodel_name='clouder.certificate.authority',
        required=True,
        ondelete='cascade',
    )

    @api.model
    def _compute_exec_service_id(self):
        for record in self:
            service_ids = record.service_ids.filtered(
                lambda s: s.code == 'exec',
            )
            record.exec_service_id = service_ids[0]


