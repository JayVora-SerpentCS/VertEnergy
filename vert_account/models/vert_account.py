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


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    serial_no = fields.Many2one('stock.production.lot', string="Serial Number")


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


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        self.check_limit()
        return super(account_invoice, self).action_move_create()

    @api.one
    def check_limit(self):
        tot_due = self.amount_total + self.partner_id.credit
        if self.partner_id.credit_limit < tot_due:
            raise except_orm(
                _('Credit Limit'),
                _('Validating invoice exceeds the credit limit of %s') %
                (self.partner_id.name))
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
