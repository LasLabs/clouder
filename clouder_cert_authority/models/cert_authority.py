# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import pickle

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from ..api import API

class ClouderCertAuthority(models.Model, API):
    """ It provides an interface for controlling a Cert Authority. """

    _name = 'clouder.cert.authority'
    _description = 'Clouder Cert Authority'
    _inherits = {'clouder.service': 'service_id'}

    service_id = fields.Many2one(
        string='Cert Authority',
        comodel_name='clouder.service',
        required=True,
        ondelete='cascade',
        domain=lambda s: "[('application_id.tag_ids', 'in', %s)]" % (
            s.env.ref("clouder_cert_authority.tag_cert_authority").ids,
        )
    )
    environment_id = fields.Many2one(
        string='Environment',
        comodel_name='clouder.environment',
        related='service_id.environment_id',
    )
    api_port_id = fields.Many2one(
        string='API Port',
        comodel_name='clouder.image.port',
        compute='_compute_api_port_id',
    )
    private_key_ids = fields.One2many(
        string='Private Keys',
        comodel_name='clouder.key.private',
        related='cert_request_id.private_key_ids',
    )
    cert_ids = fields.One2many(
        string='Certs',
        comodel_name='clouder.key.public',
        related='cert_request_id.public_key_ids',
    )
    cert_request_id = fields.Many2one(
        string='CSR',
        comodel_name='clouder.cert.request',
        context="""{'default_host_ids': [(4, node_id)],
                    'default_authority_id': id,
                    'default_public_key_id': cert_id,
                    }""",
        help='Cert Signing Request.',
    )
    config_id = fields.Many2one(
        string='Configuration',
        comodel_name='clouder.config.cert.server',
        help='Cert Authority Configuration.',
    )
    is_initialized = fields.Boolean(
        string='Initialized',
        readonly=True,
        help='Has this CA server been initialized yet?',
    )
    openssl_service_id = fields.Many2one(
        string='OpenSSL Service',
        comodel_name='clouder.service',
        compute='_compute_openssl_service_id',
    )

    @api.multi
    @api.depends('service_id')
    def _compute_api_port_id(self):
        for record in self:
            ports = record.service_id.port_ids.filtered(
                lambda r: r.name == 'https'
            )
            record.api_port_id = ports[0]

    @api.multi
    @api.depends('sign_default_id',
                 'sign_profile_ids',
                 )
    def _compute_auth_policy_ids(self):
        for record in self:
            policies = sum((record.sign_default_id,
                            record.sign_profile_ids,
                            ))
            record.auth_policy_ids = policies.mapped('auth_policy_id')

    @api.multi
    @api.depends('service_id')
    def _compute_openssl_service_id(self):
        for record in self:
            # @TODO
            raise NotImplementedError()

    @api.multi
    @api.constrains('environment_id', 'service_id')
    def _check_environment_id(self):
        for record in self:
            res = self.search(
                [('environment_id', '=', record.enviroment_id.id)],
            )
            if len(res) > 1:
                raise ValidationError(_(
                    'The Environment "%s" already has an active Certificate '
                    'Authority.',
                ))

    @api.multi
    def name_get(self):
        names = []
        for record in self:
            name = record.name
            if record.cert_request_id:
                name += ': %s' % record.cert_request_id.name
            names.append((record.id, name))
        return names

    @api.multi
    def init_ca(self):
        """ It initializes a new cert authority if needed. """
        for record in self.fitered(lambda r: not r.is_initialized):
            if not record.cert_request_id:
                raise ValidationError(_(
                    'You must assign a cert request before '
                    'initializing a Cert Authority.',
                ))
            with record.get_api() as api:
                csr = record.cert_request_id
                response = api.init_ca(
                    cert_request=csr.api_object,
                    ca=record.config_id.api_object,
                )
                cert = record.cert_request_id._new_cert(
                    response['cert'],
                )
                private_key = record.cert_request_id._new_key(
                    response['private_key'],
                    public=False,
                )
                record.write({
                    'is_initialized': True,
                })

    @api.multi
    def scan(self, host, ip=None):
        """ It scans servers to determine the quality of their TLS setup.

        Args:
            host (ClouderCertHost): The host to scan.
            ip (str): The IP Address to override DNS lookup of host.
        """
        self.ensure_one()
        with self.get_api() as api:
            results = api.scan(host.api_object, ip)
            if results['error']:
                raise UserError(_(results['error']))
            return {
                'grade': results['grade'],
                'output': results['output'],
            }

    @api.multi
    def sign(self, cert_request, hosts=None,
             subject=None, serial_sequence=None):
        """ It signs a cert request. """
        self.ensure_one()
        if hosts is None:
            hosts = []
        with self.get_api() as api:
            results = api.sign(
                certifcate_request=cert_request.api_object,
                profile=self.config_id.api_object,
                hosts=[host.api_object for host in hosts],
                subject=subject,
                serial_sequence=serial_sequence,
            )
            return cert_request._new_cert(results)

    @api.multi
    def revoke(self, cert):
        """ It revokes a cert. """
        self.ensure_one()
        with self.get_api() as api:
            api.revoke(cert.name, cert.authority_key)

    @api.model
    def _get_cert_info(self, cert):
        """ It returns information about a signed cert.

        Args:
            cert (str): PEM encoded cert.
        Returns:
            dict: A dictionary with the following keys:
                * extensions (:class:`dict`): X.509 extensions. Some valid
                  keys are:
                    * authorityInfoAccess
                    * authorityKeyIdentifier
                    * basicConstraints
                    * cRLDistributionPoints
                    * certPolicies
                    * extendedKeyUsage
                    * issuerAltName
                    * keyUsage
                    * subjectAltName
                    * subjectKeyIdentifier
                * fingerprint (:class:`str`): Cert fingerprint.
                * signature (:class:`str`): Cert signature.
                * not_valid_before (:class:`datetime`): Validity start
                  date for the cert.
                * not_valid_after (:class:`datetime`): Validity end date
                  for the cert.
                * public_key (:class:`str`): Public key associated with
                  the cert.
        """
        self.ensure_one()
        res = self.openssl_service_id.execute(['parse_cert', cert])
        return pickle.loads(res.decode('base64'))
