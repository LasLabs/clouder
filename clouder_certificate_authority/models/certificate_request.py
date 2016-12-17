# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from hashlib import sha1

from odoo import api, fields, models

from ..api import API


class ClouderCertificateRequest(models.Model, API):
    """ It provides the concept of a Certificate Request """

    _name = 'clouder.certificate.request'
    _inherit = ['clouder.certificate.abstract',
                'clouder.key.abstract',
                ]
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
    public_key_ids = fields.One2many(
        string='Public Key',
        comodel_name='clouder.key.public',
        inverse_name='request_id',
    )
    private_key_ids = fields.One2many(
        string='Private Key',
        comodel_name='clouder.key.private',
        inverse_name='request_id',
    )
    certificate_ids = fields.One2many(
        string='Signed Certificate',
        comodel_name='clouder.certificate',
        inverse_name='request_id',
    )
    api_object = fields.Binary(
        compute="_compute_api_object",
    )

    @api.multi
    def create_cert(self):
        for record in self:
            with record.get_api(record.authority_id) as api:
                response = api.new_cert(
                    request=record.to_api(),
                )
                certificate = record._new_cert(
                    response['certificate'],
                )
                private_key = record._new_key(
                    response['private_key'],
                    public=True,
                )
                attachment = record.attachment_id.create({
                    'datas': response['certificate_request'],
                })
                record.write({
                    'attachment_id': attachment.id,
                })

    @api.multi
    def _new_key(self, key_data, public=False, mime='x-pem-file'):
        self.ensure_one()
        model = 'public' if public else 'private'
        key = self.env['clouder.key.%s' % model].create({
            'name': sha1(key_data).hexdigest(),
            'strength': self.strength,
            'algorithm': self.algorithm,
            'mime_sub_type': mime,
            'request_id': self.id,
        })
        attachment = key.attachment_id.create({
            'datas': key_data,
        })
        key.attachment_id = attachment.id
        return key

    @api.multi
    def _new_cert(self, cert_data):
        self.ensure_one()
        cert_info = self.authority_id._get_cert_info(cert_data)
        public_key = self._new_key(
            cert['public_key'],
            public=True,
        )
        auth_key = cert_info['authorityKeyIdentifier']['key_identifier']
        usages = self.env['clouder.policy.use']
        for usage_str in cert_info['keyUsage']:
            usage = usages.search([
                ('code', '=', usage_str.replace(' ', '_')),
            ])
            if not usage:
                continue
            usages += usage
        certificate = self.env['clouder.certificate.x509'].create({
            'subject_key': cert_info['subjectKeyIdentifier']['digest'],
            'authority_key': auth_key,
            'public_key_id': public_key.id,
            'request_id': self.id,
            'usage_ids': usages.ids,
        })
        attachment = key.attachment_id.create({
            'datas': cert_data,
        })
        certificate.attachment_id = attachment.id

    @api.multi
    def _compute_api_object(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.api_object = self.cfssl.CertificateRequest(
                common_name=record.name,
                names=record.subject_info_ids.mapped('api_object'),
                hosts=record.host_ids.mapped('api_object'),
                key=self.cfssl.ConfigKey(
                    algorithm=record.algorithm,
                    strength=record.strength,
                ),
            )
