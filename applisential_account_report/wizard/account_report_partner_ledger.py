# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


class account_partner_ledger(models.TransientModel):

    _inherit = 'account.partner.ledger'
    _defaults = {
       'page_split': True,
       'target_move': 'all',
    }

    @api.multi
    def _print_report(self, data):
        data = self.pre_print_report(data)
        ctx = self._context
        partner_rec = self.env['res.partner'].browse(ctx.get('active_ids'))
        data['form'].update(self.read(['initial_balance', 'filter',
                                       'page_split', 'amount_currency'])[0])
        data['form'].update({'partner_ids': ctx.get('active_ids', [])})

        if data['form']['filter'] == 'filter_no':
            data['form']['initial_balance'] = False

        if data['form']['filter'] == 'filter_period':
            pl = [data['form']['used_context']['period_from'],
                  data['form']['used_context']['period_to']]
            data['form']['used_context']['periods'] = pl
        # write initial_balance because print report with date and
        # initial_balance after that print report with no filter still
        # initial balance is ticked
        self.write({'initial_balance': data['form'].get('initial_balance',
                                                        False)})
        if data['form']['page_split']:
            return self.env['report'].get_action(partner_rec, 'applisential_account_report.customer_statement_qweb_report', data=data)

account_partner_ledger()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
