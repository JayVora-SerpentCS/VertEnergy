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
from openerp.report import report_sxw
from openerp import models, api


class vat_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(vat_report, self).__init__(cr, uid, name, context=context)
        self.sum_base_sale = 0.0
        self.sum_amount_sale = 0.0
        self.sum_base_pur = 0.0
        self.sum_amount_pur = 0.0
        self.sum_base_bank = 0.0
        self.sum_amount_bank = 0.0
        self.localcontext.update({
            'get_bank_data': self.get_bank_data,
            'get_data': self.get_data,
            'get_sum_base_bank': self._get_sum_base_bank,
            'get_sum_amount_bank': self._get_sum_amount_bank,
            'get_sum_inclusive_bank': self._get_sum_inclusive_bank,
            'get_sum_base_sale': self._get_sum_base_sale,
            'get_sum_amount_sale': self._get_sum_amount_sale,
            'get_sum_inclusive_sale': self._get_sum_inclusive_sale,
            'get_sum_base_pur': self._get_sum_base_pur,
            'get_sum_inclusive_pur': self._get_sum_inclusive_pur,
            'get_sum_amount_pur': self._get_sum_amount_pur,
            'get_net_tax': self._get_net_tax,
            'get_net_inclusive': self._get_net_inclusive
            })

    @api.v7
    def get_bank_data(self, data):
        bank_statement_line_search_ids = []
        res_list = []
        bank_statement_obj = self.pool.get('account.bank.statement')
        bank_ids = bank_statement_obj.search(
            self.cr, self.uid, [('state', '=', 'confirm')])
        for line in bank_statement_obj.browse(self.cr, self.uid, bank_ids):
            if (data['period_from'] <= line.period_id.date_start and
                    data['period_to'] >= line.period_id.date_stop):
                for rec in line.line_ids:
                    if rec.tax_id:
                        tax_amount = rec.amount * rec.tax_id.amount
                        self.sum_base_bank = rec.amount + self.sum_base_bank
                        self.sum_amount_bank = (
                            tax_amount + self.sum_amount_bank)
                        vals = {
                            'date': rec.date or True,
                            'account': (rec.account_id and rec.account_id
                                        .code or " ") + " " + (rec.account_id
                                        and rec.account_id.name or " "),
                            'ref': rec.ref or '',
                            'description': rec.tax_id.name or '',
                            'exclusive': rec.amount or 0.0,
                            'inclusive': tax_amount + rec.amount or 0.0,
                            'tax': rec.amount * rec.tax_id.amount or 0.0,
                            'customer': rec.partner_id.name or ''
                            }
                        res_list.append(vals)
                        bank_statement_line_search_ids.append(rec.id)
        return res_list

    @api.v7
    def get_data(self, data):
        self.sum_amount_pur = 0.0
        self.sum_base_pur = 0.0
        self.sum_amount_sale = 0.0
        self.sum_base_sale = 0.0
        res_list = []
        invoice_obj = self.pool.get('account.invoice')
        invoice_ids = invoice_obj.search(
            self.cr, self.uid, [('state', 'in', ('paid', 'open'))])
        for line in invoice_obj.browse(self.cr, self.uid, invoice_ids):
            if (data['period_from'] <= line.period_id.date_start and
                    data['period_to'] >= line.period_id.date_stop):
                if line.journal_id.type == data['type']:
                    if line.amount_tax:
                        if line.journal_id.type == 'sale':
                            for invoice_rec in line.invoice_line:
                                if invoice_rec.invoice_line_tax_id:
                                    self.sum_base_sale = (
                                        self.sum_base_sale +
                                        invoice_rec.price_subtotal)
                                    tax_amount_cal_sale = 0.0
                                    account_name_sale = ''
                                    tax_name = ''
                                    stx = invoice_rec.invoice_line_tax_id
                                    for tax_line in stx:
                                        tax_name = (tax_line.name + "," +
                                                    tax_name)
                                        tax_amount_cal_sale = ((
                                            invoice_rec.price_subtotal *
                                            tax_line.amount) +
                                            tax_amount_cal_sale)
                                        account_name_sale = (
                                            tax_line.account_collected_id
                                            .code + " " + tax_line
                                            .account_collected_id.name
                                            )
                                    vals = {
                                        'date': line.move_id.date or True,
                                        'type': line.journal_id.type or '',
                                        'account': account_name_sale or '',
                                        'reference': line.number or '',
                                        'description': tax_name or '',
                                        'exclusive':
                                        invoice_rec.price_subtotal or 0.0,
                                        'inclusive': tax_amount_cal_sale +
                                        invoice_rec.price_subtotal or 0.0,
                                        'tax_amount': tax_amount_cal_sale or
                                        0.0,
                                        'customer': line.partner_id.name or ''}
                                    res_list.append(vals)
                            self.sum_amount_sale += line.amount_tax
                        if line.journal_id.type == 'purchase':
                            for invoice_rec in line.invoice_line:
                                if invoice_rec.invoice_line_tax_id:
                                    self.sum_base_pur = (
                                        self.sum_base_pur + invoice_rec
                                        .price_subtotal)
                                    tax_amount_cal_pur = 0.0
                                    account_name_pur = ''
                                    tax_name = ''
                                    ltx = invoice_rec.invoice_line_tax_id
                                    for tax_line in ltx:
                                        tax_name = (tax_line.name + "," +
                                                    tax_name)
                                        tax_amount_cal_pur = ((
                                            invoice_rec.price_subtotal *
                                            tax_line.amount) +
                                            tax_amount_cal_pur)
                                        account_name_pur = (
                                            tax_line.account_collected_id
                                            .code + " " + tax_line
                                            .account_collected_id
                                            .name)
                                    vals = {
                                        'date': line.move_id.date,
                                        'type': line.journal_id.type,
                                        'account': account_name_pur,
                                        'reference': line.number or '',
                                        'description': tax_name,
                                        'exclusive':
                                        invoice_rec.price_subtotal,
                                        'inclusive': tax_amount_cal_pur +
                                        invoice_rec.price_subtotal,
                                        'tax_amount': tax_amount_cal_pur,
                                        'customer': line.partner_id.name or ''}
                                    res_list.append(vals)
                            self.sum_amount_pur += line.amount_tax
                if data['type'] == 'both':
                    if (line.journal_id.type == 'sale' or
                            line.journal_id.type == 'purchase'):
                        if line.amount_tax:
                            if line.journal_id.type == 'sale':
                                for invoice_rec in line.invoice_line:
                                    if invoice_rec.invoice_line_tax_id:
                                        self.sum_base_sale = (
                                            self.sum_base_sale + invoice_rec
                                            .price_subtotal)
                                        tax_amount_cal_sale = 0.0
                                        account_name_sale = ''
                                        tax_name = ''
                                        itx = invoice_rec.invoice_line_tax_id
                                        for tax_line in itx:
                                            tax_name = (
                                                tax_line.name + "," + tax_name)
                                            tax_amount_cal_sale = ((
                                                invoice_rec.price_subtotal *
                                                tax_line.amount) +
                                                tax_amount_cal_sale)
                                            account_name_sale = (
                                                tax_line.account_collected_id
                                                .code + " " + tax_line
                                                .account_collected_id.name
                                                )
                                        vals = {
                                            'date': line.move_id.date or True,
                                            'type': line.journal_id.type or '',
                                            'account': account_name_sale or '',
                                            'reference': line.number or '',
                                            'description': tax_name or '',
                                            'exclusive':
                                            invoice_rec.price_subtotal or 0.0,
                                            'inclusive':
                                            tax_amount_cal_sale +
                                            invoice_rec.price_subtotal or 0.0,
                                            'tax_amount':
                                            tax_amount_cal_sale or 0.0,
                                            'customer':
                                            line.partner_id.name or ''}
                                        res_list.append(vals)
                                self.sum_amount_sale += line.amount_tax
                            if line.journal_id.type == 'purchase':
                                for invoice_rec in line.invoice_line:
                                    if invoice_rec.invoice_line_tax_id:
                                        self.sum_base_pur = (
                                            self.sum_base_pur +
                                            invoice_rec.price_subtotal)
                                        tax_amount_cal_pur = 0.0
                                        account_name_pur = ''
                                        tax_name = ''
                                        ptx = invoice_rec.invoice_line_tax_id
                                        for tax_line in ptx:
                                            tax_name = (tax_line.name + "," +
                                                        tax_name)
                                            tax_amount_cal_pur = ((
                                                invoice_rec.price_subtotal *
                                                tax_line.amount) +
                                                tax_amount_cal_pur)
                                            account_name_pur = (
                                                tax_line.account_collected_id
                                                .code + " " + tax_line
                                                .account_collected_id.name
                                                )
                                        vals = {
                                            'date': line.move_id.date,
                                            'type': line.journal_id.type,
                                            'account': account_name_pur,
                                            'reference': line.number or '',
                                            'description': tax_name,
                                            'exclusive':
                                            invoice_rec.price_subtotal,
                                            'inclusive':
                                            tax_amount_cal_pur +
                                            invoice_rec.price_subtotal,
                                            'tax_amount':
                                            tax_amount_cal_pur,
                                            'customer':
                                            line.partner_id.name or ''}
                                        res_list.append(vals)
                                self.sum_amount_pur += line.amount_tax
        return res_list

    def _get_sum_base_bank(self):
        return self.sum_base_bank

    def _get_sum_amount_bank(self):
        return self.sum_amount_bank

    def _get_sum_inclusive_bank(self):
        return self.sum_base_bank + self.sum_amount_bank

    def _get_sum_base_sale(self):
        return self.sum_base_sale

    def _get_sum_amount_sale(self):
        return self.sum_amount_sale

    def _get_sum_inclusive_sale(self):
        return self.sum_base_sale + self.sum_amount_sale

    def _get_sum_base_pur(self):
        return self.sum_base_pur

    def _get_sum_amount_pur(self):
        return self.sum_amount_pur

    def _get_sum_inclusive_pur(self):
        return self.sum_base_pur + self.sum_amount_pur

    def _get_net_inclusive(self):
        return ((self.sum_base_sale + self.sum_amount_sale) +
                (self.sum_base_pur + self.sum_amount_pur))

    def _get_net_tax(self):
        return self.sum_amount_sale + self.sum_amount_pur


class report_vat(models.AbstractModel):
    _name = 'report.vert_vat_report.vat_report'
    _inherit = 'report.abstract_report'
    _template = 'vert_vat_report.vat_report'
    _wrapped_report_class = vat_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
