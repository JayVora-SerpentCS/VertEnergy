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

from openerp import models
from openerp.report.report_sxw import rml_parse


class stock_move_parser(rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(stock_move_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_received_quantity': self.get_received_quantity,
            'get_available_quantity': self.get_available_quantity
            })

    def get_received_quantity(self, data):
        total_qty = 0.0
        for rec in data:
            for rec1 in rec.move_ids:
                if rec1.state == 'done':
                    total_qty += rec1.product_uom_qty
        return total_qty

    def get_available_quantity(self, data):
        quantity = 0.0
        for rec in data:
            for rec1 in rec.move_ids:
                if rec1.state == 'assigned':
                    quantity = rec1.product_uom_qty
        return quantity


class stock_move_abstract(models.AbstractModel):
    _name = 'report.vert_stock.vert_stock_move_product_report'
    _inherit = 'report.abstract_report'
    _template = 'vert_stock.vert_stock_move_product_report'
    _wrapped_report_class = stock_move_parser

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
