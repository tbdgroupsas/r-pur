# -*- coding: utf-8 -*-


from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    unit_cost = fields.Float(string='Unit Cost', related = 'product_id.standard_price')
    lst_price = fields.Float(string='Unit Price', related = 'product_id.lst_price')
    
    value_price = fields.Float(string='Value Price', compute='_compute_value_price', readonly=True)
    
        
    @api.depends('product_id.lst_price','inventory_quantity')
    def _compute_value_price(self):
        for record in self:
            if record.inventory_quantity >= 0:
                record.value_price = record.product_id.lst_price * record.inventory_quantity
            else:
                record.value_price = 0
                

