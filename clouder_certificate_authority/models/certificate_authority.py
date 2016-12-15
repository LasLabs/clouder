# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ClouderCertificateAuthority(models.Model):
    """ It provides an interface for controlling a Cert Authority """

    _name = 'clouder.certificate.authority'
    _description = 'Clouder Certificate Authority'
    _inherits = {'clouder.application': 'application_id'}

    application_id = fields.Many2one(
        string='Application',
        comodel_name='clouder.application',
        required=True,
        ondelete='cascade',
        domain=lambda s: "[('tag_ids', '=', %d)]" % s.enf.ref(
            'clouder_certificate_authority.tag_cert_authority',
        ),
    )
    exec_service_id = fields.Many2one(
        string='Executor Service',
        comodel_name='clouder.service',
        compute='_compute_exec_service_id',
    )

    @api.model
    def _compute_exec_service_id(self):
        for record in self:
            service_ids = record.service_ids.filtered(
                lambda s: s.code == 'exec',
            )
            record.exec_service_id = service_ids[0]


