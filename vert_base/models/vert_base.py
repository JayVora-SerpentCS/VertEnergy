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

from openerp import models, fields


class res_partner(models.Model):
    _inherit = 'res.partner'

    cust_acc_ref = fields.Char(string='Customer Acc. Ref. No.')
    supp_acc_ref = fields.Char(string='Supplier Acc. Ref. No.')
    vat_no = fields.Char(string="Vat No.")
    company_reg = fields.Char(string="Company Reg")


class sale_order(models.Model):
    _inherit = 'sale.order'

    sale_cust_acc_ref = fields.Char(string='Customer Acc. Ref. No.')


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    pur_supp_acc_ref = fields.Char(string='Supplier Acc. Ref. No.')


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    inv_cust_acc_ref = fields.Char(string='Customer Acc. Ref. No.')
    inv_supp_acc_ref = fields.Char(string='Supplier Acc. Ref. No.')
