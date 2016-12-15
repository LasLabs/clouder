# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class ClouderConfigCertificateServer(models.Model):
    """ It provides data handling for certificate server configs. """

    _name = 'clouder.config.certificate.server'
    _inherit = 'clouder.config.certificate.abstract'
    _description = 'Clouder Config Certificate Server'
