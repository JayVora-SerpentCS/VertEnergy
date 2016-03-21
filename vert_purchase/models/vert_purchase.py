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


class purchase_availability(models.Model):
    _name = 'purchase.availability'
    _description = 'Purchase Availability'

    name = fields.Char(string='Availability')


class purchase_shipping_duration(models.Model):
    _name = 'purchase.shipping.duration'
    _description = 'Shipping Duration'

    name = fields.Char(string='Shipping Duration')


class purchase_rate_exchange(models.Model):
    _name = 'purchase.rate.exchange'
    _description = 'Rate of Exchange'

    name = fields.Char(string='Rate of Exchange')


class purchase_quotation_validity(models.Model):
    _name = 'purchase.quotation.validity'
    _description = 'Quotation Validity'

    name = fields.Char(sting='Quotation Validity')


class purchase_forward_exchange_contract(models.Model):
    _name = 'purchase.forward.exchange.contract'
    _description = 'Forward Exchange Contract'

    name = fields.Char(string='Forward Exchange Contract')


class purchase_deposits(models.Model):
    _name = 'purchase.deposits'
    _description = 'Purchase Deposits'

    name = fields.Char(string='Deposits')


class purchase_balance_payable(models.Model):
    _name = 'purchase.balance.payable'
    _description = 'Balance Payable'

    name = fields.Char(string='Balance Payable')


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    inco_name = fields.Char(string='Incoterms Place')
    availibility = fields.Many2one('purchase.availability',
                                   string='Availability')
    ship_dur = fields.Many2one('purchase.shipping.duration',
                               string='Shipping Duration')
    quot_validity = fields.Many2one('purchase.quotation.validity',
                                    string='Quotation Validity')
    ex_rate = fields.Many2one('purchase.rate.exchange',
                              string='Rate of Exchange')
    ex_contract = fields.Many2one('purchase.forward.exchange.contract',
                                  string='Forward Exchange Contract')
    deposit = fields.Many2one('purchase.deposits', string='Deposits')
    bal_pay = fields.Many2one('purchase.balance.payable',
                              string='Balance Payable')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
