from odoo import api, fields, models



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_category = fields.Char(string='Product Category', 
                                      compute='_compute_product_category', readonly=True, store=True)
    
    
    @api.depends('product_id.categ_id')
    def _compute_product_category(self):
        for record in self:
            record.product_category = record.product_id.categ_id.display_name
    
    
    invoice_date_due = fields.Date(string='Invoice Due Date', 
                                   compute="_compute_invoice_date_due", readonly=True, store=True)

    @api.depends('move_id.invoice_date_due')
    def _compute_invoice_date_due(self):
        for record in self:
            record.invoice_date_due = record.move_id.invoice_date_due
