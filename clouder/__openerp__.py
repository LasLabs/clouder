# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Buron
#    Copyright 2015 Yannick Buron
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Clouder',
    'version': '1.0',
    'category': 'Community',
    'depends': ['base'],
    'author': 'Yannick Buron',
    'license': 'AGPL-3',
    'website': 'https://github.com/YannickB',
    'description': """
    Clouder
    """,
    'demo': [],
    'data': [
        'clouder_view.xml',
        'data/clouder_data.xml',
        'clouder_template_archive/clouder_template_archive_data.xml',
        'clouder_template_backup/clouder_template_backup_data.xml',
        'clouder_template_registry/clouder_template_registry_data.xml'
    ],
    'installable': True,
    'application': True,
}