# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-TODAY Serpent Consulting Services Pvt.Ltd.
#    (<http://www.serpentcs.com>).
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
    'name': 'Vert Sales Management',
    'version': '1.0',
    'category': 'Sales Management',
    'description': """
        This module is used for customization of sales quotations and orders
     """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['sale_stock', 'vert_base', 'vert_product'],
    'data': [
        'data/available_data.xml',
        'data/shipping_duration_data.xml',
        'data/quotation_validity_data.xml',
        'data/rate_exchange_data.xml',
        'data/forward_exchange_contract_data.xml',
        'data/sale_deposits_data.xml',
        'data/balance_payable_data.xml',
        'views/vert_sale_view.xml',
        'security/ir.model.access.csv',
        'views/vert_sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
