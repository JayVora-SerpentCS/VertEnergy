from openerp import models, fields


class product_template(models.Model):
    _inherit = "product.template"
    _description = "Product Template"

    length = fields.Float(string='Length(mm)')
    width = fields.Float(string='Width  (mm)')
    height = fields.Float(string='Height(mm)')
    coo = fields.Char(string='Country of Origin')
    cth = fields.Char(string='Customs Tariff Heading')
