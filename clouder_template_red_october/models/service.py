# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ClouderService(models.Model):
    _inherit = 'clouder.service'

    @api.multi
    def deploy_post(self):
        super(ClouderService, self).deploy_post()
        for record in self:
            if record.application_id.type_id.name == 'redoctober':
                if record.application_id.code == 'data':
                    # @TODO: Create a CSR, sign it with the CA, execute echo
                    pass
