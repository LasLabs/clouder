# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Clouder Template Elasticsearch',
    'version': '9.0.10.0.0',
    'category': 'Clouder',
    'depends': [
        'clouder',
        'clouder_template_proxy',
    ],
    'author': 'LasLabs Inc.',
    'license': 'LGPL-3',
    'website': 'https://github.com/clouder-community/clouder',
    'data': [
        'data/image_template.xml',
        'data/image.xml',
        'data/image_port.xml',
        'data/image_volume.xml',
        'data/application_type.xml',
        'data/application_type_option.xml',
        'data/application_template.xml',
        'data/application.xml',
        'data/application_link.xml',
    ],
    'installable': True,
    'application': False,
}
