# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Serpent Consulting Services Pvt.Ltd.
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


class crm_claim(models.Model):
    _inherit = 'crm.claim'

    ref1 = fields.Reference(string='Partner',
                            selection=[('res.partner', 'Partner')])
    ref2 = fields.Reference(string='Product',
                            selection=[('product.product', 'Product')])
    ref3 = fields.Reference(string='Invoice',
                            selection=[('account.invoice', 'Invoice')])
    ref4 = fields.Reference(string='Sales Order',
                            selection=[('sale.order', 'Sales Order')])
    ref5 = fields.Reference(string='Serial Numbers',
                        selection=[('stock.production.lot', 'Serial Number')])
    ref6 = fields.Reference(string='Purchase Order',
                            selection=[('purchase.order', 'Purchase Order')])
    rpt_ref = fields.Char(string='Report Ref.')
    ins_date = fields.Datetime('Inspection Date', select=True)
    inspected_by = fields.Many2one('hr.employee', string='Inspected by')
    approved_by = fields.Many2one('hr.employee', string='Approved by')
