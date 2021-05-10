# -*- coding: utf-8 -*-

import re
from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from odoo.osv.expression import AND, expression


class PurchaseReportCustom(models.Model):
    _inherit = 'purchase.report'
    _auto = False

    due_date = fields.Datetime('Due Date', readonly=True)

    def _select(self):
        return super(PurchaseReportCustom, self)._select() + ", am.invoice_date_due as due_date"

    def _from(self):
        return super(PurchaseReportCustom, self)._from() + " left join account_move_purchase_order_rel ampor on (l.order_id = ampor.purchase_order_id) \
                left join account_move am on (ampor.account_move_id = am.id)"

    def _group_by(self):
        return super(PurchaseReportCustom, self)._group_by() + ", am.invoice_date_due"
