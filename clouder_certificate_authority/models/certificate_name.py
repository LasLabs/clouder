# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ClouderCertificateName(models.Model):
    """ It provides the concept of a cert's SubjectInfo """

    _name = 'clouder.certificate.name'
    _description = 'Clouder Certificate Name'

    country_id = fields.Many2one(
        string='Country',
        model='res.country',
        required=True,
        default=lambda s: s.env.user.country_id,
    )
    state_id = fields.Many2one(
        string='State',
        model='res.country.state',
        domain='[(country_id, "=", country_id)]',
        default=lambda s: s.env.user.state_id,
    )
    city = fields.Char(
        default=lambda s: s.env.user.city,
    )
    company_id = fields.Many2one(
        string='Company',
        model='res.company',
        required=True,
        domain='[(company_id, "=", company_id)]',
        default=lambda s: s.env.user.company_id,
    )
    organization_unit = fields.Char(
        required=True,
    )
    computed = fields.Serialized(
        compute="_compute_computed",
    )

    @api.multi
    def _compute_computed(self):
        """ It computes the keys required for the JSON request """
        for record in self:
            record.computed = {
                'C': record.country_id.code,
                'ST': record.state_id.name,
                'L': record.city,
                'O': record.company_id.name,
                'OU': record.organization_unit,
            }
