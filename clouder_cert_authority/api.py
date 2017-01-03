# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from contextlib import contextmanager

from odoo import api

_logger = logging.getLogger(__name__)

try:
    import cfssl
except ImportError:
    _logger.info('CFSSL Python library is not installed.')


class API(object):
    """ It provides a base for all Models requiring API functionality """

    cfssl = cfssl

    @contextmanager
    @api.model_cr_context
    def get_api(self, cert_authority=None):
        """ It returns a :obj:`cfssl.CFSSL` for the cert authority.

        Args:
            cert_authority (:type:`clouder.CertAuthority`):
                The cert authority record singleton representing the
                remote API. The CA does not have to be initialized yet. Use
                :type:`None` if ``self`` is the CA that should be connected
                to.
        """
        try:
            # @TODO: Figure out how the hell to get this host from the base
            host = '000.000.000.000'
            port = cert_authority.port_id.local_port
            api = cfssl.CFSSL(host, port, ssl=True)
            yield api
        finally:
            pass
