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

import time
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from openerp import models
from openerp.tools.translate import _
from openerp.addons.account.report.account_partner_ledger import third_party_ledger


class third_party_ledger(third_party_ledger):

    def __init__(self, cr, uid, name, context=None):
        super(third_party_ledger, self).__init__(cr, uid,
                                                 name, context=context)
        self.amt = 0.0
        self.localcontext.update({
        'get_amount_due': self.get_amount_due,
        'date_part': self.date_part,
        'get_move_data': self.get_move_data,
        'get_inv': self.get_inv,
        'get_partner_rec': self.get_partner_rec
        })
        self.lines_report = []

    def get_partner_rec(self, data):
        part_obj = self.pool.get('res.partner')
        return part_obj.browse(self.cr, self.uid, data.get('partner_ids', []))

    def get_inv(self, moveline):
        obj_move_line = self.pool.get('account.move.line')
        Invoice = obj_move_line.browse(self.cr, self.uid, moveline).invoice
        return Invoice and Invoice.origin or ''

    def lines(self, partner):
        move_obj = self.pool.get('account.move.line')
        result = super(third_party_ledger, self).lines(partner)
        print ">>>>> Resullt _>>>>>>>>>>",result,'\n','\n'
        self.lines_report = result
        sal_data = []
        for rst in result:
            paid_ref = []
            paid_date = []
            paid_amt = []
            mv_id = move_obj.browse(self.cr, self.uid, rst.get('id'))
            if mv_id.invoice:
                for payment in mv_id.invoice.payment_ids:
                    paid_ref.append(payment.move_id.name)
                    pmt_dt = payment.move_id.date
                    dt_strp = datetime.strptime(pmt_dt, '%Y-%m-%d')
                    dt_strf = dt_strp.strftime('%m-%d-%Y')
                    paid_date.append(dt_strf)
                    if mv_id.invoice.type in('out_invoice', 'out_refund'):
                        paid_amt.append(payment.credit)
                    else:
                        paid_amt.append(payment.debit)
                rst.update({'pay_ref': paid_ref and
                                ', '.join(map(str, paid_ref)) or '',
                            'date_maturity': mv_id.date_maturity or '',
                            'paid_date': paid_date
                                and ', '.join(map(str, paid_date)) or '',
                            'due_amount': mv_id.invoice.residual or '',
                            'paid_amt': paid_amt and
                                ', '.join(map(str, paid_amt)) or ''})
                sal_data.append(rst)
        return sal_data

    def get_amount_due(self, partner):
        print "((((((((((( call get_amount_due ))))))))))))))))))))))",'\n'
        amount_due = 0.0
        move_state = ['draft', 'posted']
        if self.target_move == 'posted':
            move_state = ['posted']
        full_account = []
        if self.reconcil:
            RECONCILE_TAG = " "
        else:
            RECONCILE_TAG = "AND l.reconcile_id IS NULL"
        self.cr.execute(
            "SELECT l.id, l.date, j.code, acc.code as a_code,"\
            "acc.name as a_name, l.ref, m.name as move_name, l.name,"\
            "l.debit, l.credit, l.amount_currency,l.currency_id,"\
            "c.symbol AS currency_code " \
            "FROM account_move_line l " \
            "LEFT JOIN account_journal j " \
                "ON (l.journal_id = j.id) " \
            "LEFT JOIN account_account acc " \
                "ON (l.account_id = acc.id) " \
            "LEFT JOIN res_currency c ON (l.currency_id=c.id)" \
            "LEFT JOIN account_move m ON (m.id=l.move_id)" \
            "WHERE l.partner_id = %s " \
                "AND l.account_id IN %s AND " + self.query + " " \
                "AND m.state IN %s " \
                " " + RECONCILE_TAG + " "\
                "ORDER BY l.date",
                (partner.id, tuple(self.account_ids), tuple(move_state)))
        res = self.cr.dictfetchall()
        dc_sum = 0.0
        if self.initial_balance:
            dc_sum = self.init_bal_sum
        for r in res:
            dc_sum += r['debit'] - r['credit']
            r['progress'] = dc_sum
            full_account.append(r)
        if full_account:
            for ln in full_account:
                pass
            else:
                last_line = ln
            amount_due = last_line['progress']
            #date_today = date.today()
        return {'amount_due': amount_due}

    # Remove partner from then argument : def date_part(self, partner)
    def date_part(self):
        res = {}
        date_data = []
        today = date.today()
        if today:
            start = today - timedelta(1)
        else:
            start = datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        period_length = 30
        for i in range(5)[::-1]:
            stop = start - relativedelta(days=period_length)
            res[str(i)] = {
                'name': (i != 0 and i != 1 and
                         (str((5 - (i + 1)) * period_length)
                              + '-' + str((5 - i) * period_length)) or
                              ('+' + str(3 * period_length))),
                'stop': start.strftime('%Y-%m-%d'),
                'start': (i != 0 and i != 1 and stop.strftime('%Y-%m-%d') or
                          False),
            }
            start = stop - relativedelta(days=1)
        date_data.append(res)
        return date_data

    def get_move_data(self, start_date, stop_date):
        amount = 0.0
        date_maturity = ''
        obj_move_line = self.pool.get('account.move.line')
        inv_obj = self.pool.get('account.invoice')
        for line in self.lines_report:
            move_id = obj_move_line.browse(self.cr, self.uid,
                                           line['id']).move_id.id
            date_maturity = obj_move_line.browse(self.cr, self.uid,
                                                 line['id']).date_maturity
            reconcile_partial_id = obj_move_line.browse(self.cr, self.uid,
                                                        line['id']
                                                        ).reconcile_partial_id
            reconcile_id = obj_move_line.browse(self.cr, self.uid, line['id']
                                                ).reconcile_id
            if date_maturity and reconcile_partial_id:
                self.cr.execute(""" UPDATE account_move_line
                                    SET date_maturity=%s where
                                    reconcile_partial_id=%s""",
                                    (date_maturity, reconcile_partial_id.id))
            if reconcile_id and date_maturity:
                self.cr.execute(""" UPDATE account_move_line
                                    SET date_maturity=%s where
                                    reconcile_id=%s""",
                                    (date_maturity, reconcile_id.id))

            if date_maturity and line['debit'] and reconcile_partial_id:
                invoice_id = inv_obj.search(self.cr, self.uid,
                                            [('move_id', '=', move_id)])
                for rec in inv_obj.browse(self.cr, self.uid, invoice_id):
                    date = rec.date_invoice
                    self.cr.execute(""" UPDATE account_move_line
                                        SET date_invoice_ref=%s where
                                        reconcile_partial_id=%s""",
                                        (date, reconcile_partial_id.id))
            if date_maturity and line['debit'] and reconcile_id:
                invoice_id = inv_obj.search(self.cr, self.uid,
                                            [('move_id', '=', move_id)])
                for rec in inv_obj.browse(self.cr, self.uid, invoice_id):
                    date = rec.date_invoice
                    self.cr.execute(""" UPDATE account_move_line
                                        SET date_invoice_ref=%s where
                                        reconcile_id=%s""",
                                        (date, reconcile_id.id))
            if date_maturity and line['debit'] and not reconcile_partial_id \
            and not reconcile_id:
                invoice_id = inv_obj.search(self.cr, self.uid,
                                            [('move_id', '=', move_id)])
                for rec in inv_obj.browse(self.cr, self.uid, invoice_id):
                    date = rec.date_invoice
                    self.cr.execute(""" UPDATE account_move_line
                                        SET date_invoice_ref=%s
                                        where id=%s""", (date, line['id']))
            date_invoice_ref = obj_move_line.browse(self.cr, self.uid,
                                                    line['id']
                                                    ).date_invoice_ref
            if date_maturity:
                if date_invoice_ref <= stop_date and \
                date_invoice_ref >= start_date:
                    amount += line['debit'] - line['credit']
                    print " FIRST     AMOUNT .>>>>>>>>>>>>>>>>>>>>",amount 
        print " RETURN AMOUNT .>>>>>>>>>>>>>>>>>>>>",amount
        return amount


class report_generic_extra(models.AbstractModel):
    _name = 'report.applisential_account_report.customer_statement_qweb_report'
    _inherit = 'report.abstract_report'
    _template = 'applisential_account_report.customer_statement_qweb_report'
    _wrapped_report_class = third_party_ledger
