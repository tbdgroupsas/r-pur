# -*- coding: utf-8 -*-

import re
from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from odoo.osv.expression import AND, expression


class PurchaseReportCustom(models.Model):
    _name = 'purchase.report'
    _inherit = 'purchase.report'
    _auto = False
    due_date = fields.Datetime('Due Date', readonly=True)

    def _select(self):
        select_str = """
        WITH currency_rate as (%s)
                        SELECT
                        po.id as order_id,
                        min(l.id) as id,
                        po.date_order as date_order,
                        po.state,
                        po.date_approve,
                        po.dest_address_id,
                        po.partner_id as partner_id,
                        po.user_id as user_id,
                        po.company_id as company_id,
                        po.fiscal_position_id as fiscal_position_id,
                        l.product_id,
                        p.product_tmpl_id,
                        t.categ_id as category_id,
                        po.currency_id,
                        t.uom_id as product_uom,
                        extract(epoch from age(po.date_approve,po.date_order))/(24*60*60)::decimal(16,2) as delay,
                        extract(epoch from age(l.date_planned,po.date_order))/(24*60*60)::decimal(16,2) as delay_pass,
                        count(*) as nbr_lines,
                        sum(l.price_total / COALESCE(po.currency_rate, 1.0))::decimal(16,2) as price_total,
                        (sum(l.product_qty * l.price_unit / COALESCE(po.currency_rate, 1.0))/NULLIF(sum(l.product_qty/line_uom.factor*product_uom.factor),0.0))::decimal(16,2) as price_average,
                        partner.country_id as country_id,
                        partner.commercial_partner_id as commercial_partner_id,
                        analytic_account.id as account_analytic_id,
                        sum(p.weight * l.product_qty/line_uom.factor*product_uom.factor) as weight,
                        sum(p.volume * l.product_qty/line_uom.factor*product_uom.factor) as volume,
                        sum(l.price_subtotal / COALESCE(po.currency_rate, 1.0))::decimal(16,2) as untaxed_total,
                        sum(l.product_qty / line_uom.factor * product_uom.factor) as qty_ordered,
                        sum(l.qty_received / line_uom.factor * product_uom.factor) as qty_received,
                        sum(l.qty_invoiced / line_uom.factor * product_uom.factor) as qty_billed,
                        case when t.purchase_method = 'purchase' 
                        then sum(l.product_qty / line_uom.factor * product_uom.factor) - sum(l.qty_invoiced / line_uom.factor * product_uom.factor)
                        else sum(l.qty_received / line_uom.factor * product_uom.factor) - sum(l.qty_invoiced / line_uom.factor * product_uom.factor)
                        end as qty_to_be_billed,
                        am.invoice_date_due as due_date
        
        """ % self.env['res.currency']._select_companies_rates()
        return select_str

    def _from(self):
        from_str = """
            purchase_order_line l
                                join purchase_order po on (l.order_id=po.id)
                                join res_partner partner on po.partner_id = partner.id
                                left join product_product p on (l.product_id=p.id)
                                left join product_template t on (p.product_tmpl_id=t.id)
                                left join uom_uom line_uom on (line_uom.id=l.product_uom)
                                left join uom_uom product_uom on (product_uom.id=t.uom_id)
                                left join account_analytic_account analytic_account on (l.account_analytic_id = analytic_account.id)
                                left join currency_rate cr on (cr.currency_id = po.currency_id and
                                cr.company_id = po.company_id and
                                cr.date_start <= coalesce(po.date_order, now()) and
                                (cr.date_end is null or cr.date_end > coalesce(po.date_order, now())))
                                left join account_move_purchase_order_rel ampor on (l.order_id = ampor.purchase_order_id)
                                left join account_move am on (ampor.account_move_id = am.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
             GROUP BY
                po.company_id,
                po.user_id,
                po.partner_id,
                line_uom.factor,
                po.currency_id,
                l.price_unit,
                po.date_approve,
                l.date_planned,
                l.product_uom,
                po.dest_address_id,
                po.fiscal_position_id,
                l.product_id,
                p.product_tmpl_id,
                t.categ_id,
                po.date_order,
                po.state,
                line_uom.uom_type,
                line_uom.category_id,
                t.uom_id,
                t.purchase_method,
                line_uom.id,
                product_uom.factor,
                partner.country_id,
                partner.commercial_partner_id,
                analytic_account.id,
                po.id,
                am.invoice_date_due
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                        %s
                        FROM ( %s )
                        %s
                        )""" % (self._table, self._select, self._from(), self._group_by()))
