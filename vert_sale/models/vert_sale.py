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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm


class sale_availability(models.Model):
    _name = 'sale.availability'
    _description = 'Sale Availability'

    name = fields.Char(string='Availability')


class sale_shipping_duration(models.Model):
    _name = 'sale.shipping.duration'
    _description = 'Shipping Duration'

    name = fields.Char(string='Shipping Duration')


class sale_rate_exchange(models.Model):
    _name = 'sale.rate.exchange'
    _description = 'Rate of Exchange'

    name = fields.Char(string='Rate of Exchange')


class sale_quotation_validity(models.Model):
    _name = 'sale.quotation.validity'
    _description = 'Quotation Validity'

    name = fields.Char(sting='Quotation Validity')


class sale_forward_exchange_contract(models.Model):
    _name = 'sale.forward.exchange.contract'
    _description = 'Forward Exchange Contract'

    name = fields.Char(string='Forward Exchange Contract')


class sale_deposits(models.Model):
    _name = 'sale.deposits'
    _description = 'sale_deposits'

    name = fields.Char(string='Deposits')


class sale_balance_payable(models.Model):
    _name = 'sale.balance.payable'
    _description = 'Balance Payable'

    name = fields.Char(string='Balance Payable')


class sale_order(models.Model):
    _inherit = 'sale.order'

    inco_name = fields.Char(string='Incoterms Place')
    availibility = fields.Many2one('sale.availability', string='Availability')
    ship_dur = fields.Many2one('sale.shipping.duration',
                               string='Shipping Duration')
    quot_validity = fields.Many2one('sale.quotation.validity',
                                    string='Quotation Validity')
    ex_rate = fields.Many2one('sale.rate.exchange', string='Rate of Exchange')
    ex_contract = fields.Many2one('sale.forward.exchange.contract',
                                  string='Forward Exchange Contract')
    deposit = fields.Many2one('sale.deposits', string='Deposits')
    bal_pay = fields.Many2one('sale.balance.payable', string='Balance Payable')

    @api.v7
    def _prepare_order_line_procurement(self,
                                        cr, uid, order,
                                        line, group_id=False, context=None):
        res = super(sale_order, self)._prepare_order_line_procurement(
            cr, uid, order, line, group_id=group_id, context=context)
        res.update({'serial_no': line.serial_no.id})
        return res

    @api.multi
    def action_wait(self):
        self.check_limit()
        return super(sale_order, self).action_wait()

    @api.one
    def check_limit(self):
        tot_due = self.amount_total + self.partner_id.credit
        if self.partner_id.credit_limit < tot_due:
            raise except_orm(
                _('Credit Limit'),
                _('Validating order exceeds the credit limit of %s') %
                (self.partner_id.name))
        return True


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sales Order Line'

    serial_no = fields.Many2one('stock.production.lot', string="Serial Number")

    @api.v7
    def _prepare_order_line_invoice_line(self, cr, uid, line,
                                         account_id=False, context=None):
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(
            cr, uid, line, account_id=account_id, context=context)
        res.update({'serial_no': line.serial_no.id})
        return res


class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    access = fields.Boolean("Access")

    @api.v7
    def default_get(self, cr, uid, fields, context=None):
        record_id = context.get('active_id')
        res = super(stock_production_lot, self).default_get(
            cr, uid, fields, context=context)
        if 'product_id' in fields and record_id:
            res.update({'product_id': record_id, 'access': True})
        return res


class crm_case_section(models.Model):
    _inherit = "crm.case.section"

    company_id = fields.Many2one("res.company", "Company")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
