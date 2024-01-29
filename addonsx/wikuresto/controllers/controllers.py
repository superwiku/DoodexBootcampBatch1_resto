# -*- coding: utf-8 -*-
# from odoo import http


# class Wikuresto(http.Controller):
#     @http.route('/wikuresto/wikuresto', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wikuresto/wikuresto/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wikuresto.listing', {
#             'root': '/wikuresto/wikuresto',
#             'objects': http.request.env['wikuresto.wikuresto'].search([]),
#         })

#     @http.route('/wikuresto/wikuresto/objects/<model("wikuresto.wikuresto"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wikuresto.object', {
#             'object': obj
#         })
