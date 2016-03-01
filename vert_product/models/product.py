# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Serpent Consulting Services Pvt.Ltd.
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

from opeerp import models, fields


class product_template(models.Model):
    _inherit = "product.template"
    _description = "Product Template"

    length = fields.Float(string='Length(mm)')
    width = fields.Float(string='Width  (mm)')
    height = fields.Float(string='Height(mm)')
    coo = fields.Char(string='Country of Origin')
    cth = fields.Char(string='Customs Tariff Heading')
