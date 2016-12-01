# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale - Clouder",
    "summary": "Provides the ability to sell Clouder instances.",
    "version": "9.0.1.0.0",
    "category": "Clouder",
    "website": "https://github.com/clouder-community/clouder",
    "author": "LasLabs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "clouder",
        "contract",
        "sale",
    ],
    "data": [
        "data/contract_line_qty_formula.xml",
    ],
}
