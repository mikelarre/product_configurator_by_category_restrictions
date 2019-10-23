# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models



# class SaleOrder(models.Model):
#     _inherit = "sale.order"
#
#     possible_next_product_ids = fields.Many2many(
#         comodel_name="product.product", compute="_next_product_ids")
#
#     @api.multi
#     def _get_next_products(self):
#         self.ensure_one()
#         product_obj = self.env['product.product']
#         last_line = self.order_line.sorted("sequence")[-1:]
#         if not last_line or last_line.display_type:
#             return None
#         last_line_categ_id = last_line.product_id.categ_id
#         restricts = last_line.product_id.restricted_products._ids
#         # restricted_to_categories = self.env['category.restrict'].search([
#         #     'restricts_to', '=', last_line_categ_id.id])
#         return product_obj.search(
#             [('id', 'in', restricts)])
#
#     @api.depends("order_line")
#     def _next_product_ids(self):
#             for order in self:
#                 next_products = order._get_next_products()
#                 if next_products:
#                     self.possible_next_product_ids = [
#                         (6, 0,  next_products._ids)
#                     ]


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_last_line(self):
        last_line = self.order_id.order_line.filtered(
            lambda x: x.product_id or x.display_type=='line_section').sorted(
            "sequence")[-1:]
        return last_line

    @api.multi
    def _get_domain(self):
        self.ensure_one()
        last_line = self._get_last_line()
        restricts = last_line.product_id.restricted_products.id
        if restricts or not last_line.display_type == 'line_section':
            return restricts
        return False
        # order = self.order_id
        # last_line = order.order_line.sorted("sequence")[-1:]
        # if self.id == last_line.id:
        #     return self.order_id.possible_next_product_ids._ids
        # return []

    @api.onchange("product_id")
    def onchange_order_line(self):
        domain = self._get_domain()
        if domain:
            return {'domain': {'product_id': [
                ('id', 'in', domain)
            ]}}

    # @api.onchange
    # def _get_domain_ext(self):
    #     self.ensure_one()
    #     order = self.order_id
    #     last_line = order.order_line.sorted("sequence")[-1:]

    # @api.onchange("sequence")
    # def onchange_sequence(self):
    #     if not self.product_id:
    #         return {{'domain': {'product_id': domain}}
    #             'id', 'in', self._get_domain_ext()
    #         }
