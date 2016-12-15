# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json

from odoo import api, fields, models


class ClouderCertificateRequest(models.Model):
    """ It provides the concept of a Certificate Request """

    _name = 'clouder.certificate.request'
    _inherit = 'clouder.certificate.abstract'
    _description = 'Clouder Certificate Request'

    name = fields.Char(
        string='Common Name',
        required=True,
    )
    authority_id = fields.Many2one(
        string='Cert Authority',
        comodel_name='clouder.certificate.authority',
        required=True,
        ondelete='cascade',
    )
    host_ids  = fields.Many2one(
        string='Hosts',
        comodel_name='clouder.certificate.host',
    )
    subject_info_ids = fields.Many2many(
        string='Names',
        comodel_name='clouder.certificate.name',
        required=True,
    )
    public_key_id = fields.Many2one(
        string='Public Key',
        comodel_name='clouder.key.public',
    )
    strength = fields.Integer(
        default=4096,
        required=True,
    )
    algorithm = fields.Selection(
        default='rsa',
        selection=lambda s: s.env['clouder.key.abstract']._get_algorithms(),
    )
    computed = fields.Serialized(
        compute="_compute_computed",
    )

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.computed = {
                'CN': record.name,
                'names': [
                    name.computed for name in record.subject_info_ids
                ],
                'hosts': [
                    '%s:%s' % (h.host, h.port) for h in record.host_ids
                ],
                'key': {
                    'algo': record.algorithm,
                    'size': record.strength,
                },
            }

    @api.multi
    def to_json(self):
        """ It returns the JSON representation of this object """
        self.ensure_one()
        return json.dumps(self.computed)
