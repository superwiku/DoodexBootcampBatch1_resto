from odoo import models, fields, api

class RestoBahan(models.Model):
    _name = 'resto.bahan'
    _description = 'RestoBahan'
    name = fields.Char(string='Nama Bahan')
    stok = fields.Integer(string='Stok', default=0)
    restomakanan_id = fields.Many2one(comodel_name='resto.makanan', string='Makanannya')
    restominuman_id = fields.Many2one(comodel_name='resto.minuman', string='Minumannya')
    
    
    
    
