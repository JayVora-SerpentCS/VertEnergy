# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
#    Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp import models, fields, api, _


class report_vat(models.TransientModel):
    _name = 'report.vat'
    _description = "Vat Report Wizard"

    period_from = fields.Date(string='Period From')
    period_to = fields.Date(string='Period To')
    type = fields.Selection([('sale', 'Sale'), ('purchase', 'Payment'),
                             ('both', 'Both')], string='Type')

    @api.multi
    def _check_date(self):
        for vat_wiz in self:
            if vat_wiz.period_from and vat_wiz.period_to:
                if vat_wiz.period_from > vat_wiz.period_to:
                    return False
        return True

    _constraints = [(_check_date, _('Please select appropriate date range!'),
                     ['period_from'])]

    @api.v7
    def print_vat_report(self, cr, uid, ids, context=None):
        res = {'ids': ids, 'model': 'account.invoice',
               'form': self.read(cr, uid, ids[0], context=context)}
        return self.pool['report'].get_action(
            cr, uid, [], 'vert_vat_report.vat_report', data=res,
            context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
