# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class ClouderConfigCertificateClient(models.Model):
    """ It provides data handling for certificate client configs. """

    _name = 'clouder.config.certificate.client'
    _inherit = 'clouder.config.certificate.abstract'
    _description = 'Clouder Config Certificate Client'

    remote_ids = fields.Many2many(
        string='Remotes',
        comodel_name='clouder.certificate.host',
        required=True,
    )

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request. """
        for record in self:
            super(ClouderConfigCertificateClient, record)._compute_computed()
            record.computed['remotes'] = {
                r.name: '%s:%s' % (r.host, r.port) for r in record.remote_ids
            }
