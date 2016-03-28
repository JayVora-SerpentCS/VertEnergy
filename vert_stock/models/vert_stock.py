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

from openerp import fields, models, api


class stock_move(models.Model):
    _inherit = "stock.move"

    serial_no = fields.Many2one('stock.production.lot', string="Serial Number")


class procurement_order(models.Model):
    _inherit = "procurement.order"

    serial_no = fields.Many2one('stock.production.lot', string="Serial Number")

    @api.v7
    def _run_move_create(self, cr, uid, procurement, context=None):
        vals = super(procurement_order, self)._run_move_create(
            cr, uid, procurement, context=context)
        vals.update({'serial_no': procurement.serial_no.id})
        return vals


class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    @api.v7
    def default_get(self, cr, uid, fields, context=None):
        record_id = context.get('active_id')
        res = super(stock_production_lot, self).default_get(
            cr, uid, fields, context=context)
        if 'product_id' in fields and record_id:
            res.update({'product_id': record_id})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
