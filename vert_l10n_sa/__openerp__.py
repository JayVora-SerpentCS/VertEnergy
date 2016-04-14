# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Serpent Consulting Services Pvt.Ltd.
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
    'name': 'South Africa - Accounting',
    'version': '1.0',
    'category': 'Localization/Account Charts',
    'description': """
    South Africa Accounting: Chart of Account.
    ==========================================
        South Africa Chart and Localization.
        Odoo Allows to Manage South Africa Accounting by Providing
        Three Formats of Chart of Account
        (1) Vert Energy System - Chart of Account
        (2) Vert Energy Africa - Chart of Account
        (3) Vert Amandla - Chart of Account
     """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['account_chart'],
    'data': ['data/account.account.template.csv',
             'l10n_ves_account_chart.xml',
             'l10n_ves_wizard.xml'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
