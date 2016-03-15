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
