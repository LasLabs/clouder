# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import pickle.loads

from odoo import api, fields, models
from odoo.exceptions import UserError

from ..api import API

class ClouderCertificateAuthority(models.Model, API):
    """ It provides an interface for controlling a Cert Authority. """

    _name = 'clouder.certificate.authority'
    _description = 'Clouder Certificate Authority'
    _inherits = {'clouder.service': 'service_id'}

    service_id = fields.Many2one(
        string='Certificate Authority',
        comodel_name='clouder.service',
        required=True,
        ondelete='cascade',
        domain=lambda s: "[('tag_ids', '=', %d)]" % s.enf.ref(
            'clouder_certificate_authority.tag_cert_authority',
        ),
    )
    api_port_id = fields.Many2one(
        string='API Port',
        comodel_name='clouder.image.port',
        compute='_compute_api_port_id',
    )
    host_id = fields.Many2one(
        string='Host',
        comodel_name='clouder.certificate.host',
    )
    private_key_ids = fields.One2many(
        string='Private Key',
        comodel_name='clouder.key.private',
        related='certificate_request_id.private_key_ids',
    )
    certificate_ids = fields.One2many(
        string='Certificate',
        comodel_name='clouder.key.public',
        related='certificate_request_id.public_key_ids',
    )
    certificate_request_id = fields.Many2one(
        string='CSR',
        comodel_name='clouder.certificate.request',
        context="""{'default_host_ids': [(4, host_id)],
                    'default_authority_id': id,
                    'default_public_key_id': certificate_id,
                    }""",
        help='Certificate Signing Request.',
    )
    config_id = fields.Many2one(
        string='Configuration',
        comodel_name='clouder.config.certificate.server',
        help='Certificate Authority Configuration.',
    )
    is_initialized = fields.Boolean(
        string='Initialized',
        help='Has this CA server been initialized yet?',
    )
    openssl_service_id = fields.Many2one(
        string='OpenSSL Service',
        comodel_name='clouder.service',
        compute='_compute_openssl_service_id',
    )

    @api.multi
    @api.depends('exec_service_id')
    def _compute_api_port_id(self):
        for record in self:
            ports = record.exec_service_id.port_ids.filtered(
                lambda r: r.name == 'https'
            )
            record.api_port_id = ports[0]

    @api.multi
    @api.depends('sign_policy_default_id',
                 'sign_policy_profile_ids',
                 )
    def _compute_auth_policy_ids(self):
        for record in self:
            policies = sum((record.sign_policy_default_id,
                            record.sign_policy_profile_ids,
                            ))
            record.auth_policy_ids = policies.mapped('auth_policy_id')

    @api.multi
    @api.depends('service_ids', 'service_ids.code')
    def _compute_exec_service_id(self):
        for record in self:
            service_ids = record.service_ids.filtered(
                lambda s: s.code == 'exec',
            )
            record.exec_service_id = service_ids[0]

    @api.multi
    @api.depends('exec_service_id')
    def _compute_openssl_service_id(self):
        for record in self:
            execs = record.exec_service_id.child_ids.filtered(
                lambda r: r.code == 'exec'
            )
            record.openssl_service_id = execs[0]

    @api.multi
    def init_ca(self):
        """ It initializes a new certificate authority if needed. """
        for record in self.fitered(lambda r: not r.is_initialized):
            with record.get_api() as api:
                csr = record.certificate_request_id
                response = api.init_ca(
                    certificate_request=csr.to_api(),
                    ca=record.config_id.to_api(),
                )
                certificate = record.certificate_request_id._new_cert(
                    response['certificate'],
                )
                private_key = record.certificate_request_id._new_key(
                    response['private_key'],
                    public=False,
                )
                record.write({
                    'is_initialized': True,
                })

    @api.multi
    def scan(self, host, ip):
        """ It scans servers to determine the quality of their TLS setup. """
        self.ensure_one()
        with self.get_api() as api:
            results = api.scan(host, ip)
            if results['error']:
                raise UserError(results['error'])
            return {
                'grade': results['grade'],
                'output': results['output'],
            }

    @api.multi
    def sign(self, certificate_request):
        """ It signs a certificate request. """
        self.ensure_one()
        with self.get_api() as api:
            results = api.sign(
                certifcate_request=certificate_request.to_api(),
                profile=self.config_id.to_api(),
            )
            return certificate_request._new_cert(results)

    @api.multi
    def revoke(self, certificate):
        """ It revokes a certificate. """
        self.ensure_one()
        with self.get_api() as api:
            api.revoke(certificate.name, certificate.authority_key)

    @api.model
    def _get_cert_info(self, cert):
        """ It returns information about a signed certificate.

        Args:
            cert (str): PEM encoded certificate.
        Returns:
            dict: A dictionary with the following keys:
                * extensions (:class:`dict`): X.509 extensions. Some valid
                  keys are:
                    * authorityInfoAccess
                    * authorityKeyIdentifier
                    * basicConstraints
                    * cRLDistributionPoints
                    * certificatePolicies
                    * extendedKeyUsage
                    * issuerAltName
                    * keyUsage
                    * subjectAltName
                    * subjectKeyIdentifier
                * fingerprint (:class:`str`): Certificate fingerprint.
                * signature (:class:`str`): Certificate signature.
                * not_valid_before (:class:`datetime`): Validity start
                  date for the certificate.
                * not_valid_after (:class:`datetime`): Validity end date
                  for the certificate.
                * public_key (:class:`str`): Public key associated with
                  the certificate.
        """
        self.ensure_one()
        res = self.openssl_service_id.execute(['parse_cert', cert])
        return pickle.loads(res.decode('base64'))
