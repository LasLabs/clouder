# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ClouderCertificateHost(models.Model):
    """ It provides the concept of a cert's CommonName """

    _name = 'clouder.certificate.host'
    _description = 'Clouder Certificate Host'

    name = fields.Char(
        required=True,
    )
    host = fields.Char(
        required=True,
    )
    port = fields.Integer()
