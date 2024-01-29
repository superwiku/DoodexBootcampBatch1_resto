from odoo import models, fields, api

class RestoMinuman(models.Model):
    _name = 'resto.minuman'
    _description = 'model.technical.name'

    name = fields.Char(string='Nama Minuman')
    restominumandetail_ids = fields.One2many(comodel_name='resto.minumandetail', inverse_name='restominuman_id', string='Bahan-bahan')
    harga = fields.Integer(string='Harga per Porsi')
    
class RestoMinumanDetail(models.Model):
    _name = 'resto.minumandetail'
    _description = 'RestoMinumanDetail'
    restobahan_id = fields.Many2one(comodel_name='resto.bahan', string='Nama Bahan')
    kebutuhan = fields.Integer(string='Kebutuhan')
    restominuman_id = fields.Many2one(comodel_name='resto.minuman', string='Makanan')