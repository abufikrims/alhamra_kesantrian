# -*- coding: utf-8 -*-
from odoo import http

# class AlhamraKesantrian(http.Controller):
#     @http.route('/alhamra_kesantrian/alhamra_kesantrian/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alhamra_kesantrian/alhamra_kesantrian/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alhamra_kesantrian.listing', {
#             'root': '/alhamra_kesantrian/alhamra_kesantrian',
#             'objects': http.request.env['alhamra_kesantrian.alhamra_kesantrian'].search([]),
#         })

#     @http.route('/alhamra_kesantrian/alhamra_kesantrian/objects/<model("alhamra_kesantrian.alhamra_kesantrian"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alhamra_kesantrian.object', {
#             'object': obj
#         })