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
        return super(PurchaseReportCustom, self)._from() + "LEFT JOIN account_move_line aml ON aml.purchase_line_id = l.id \
                LEFT JOIN account_move am ON am.id = aml.move_id  "

    def _group_by(self):
        return super(PurchaseReportCustom, self)._group_by() + ", am.invoice_date_due"
