from odoo import models, fields, api

class RestoMakanan(models.Model):
    _name = 'resto.makanan'
    _description = 'model.technical.name'

    name = fields.Char(string='Nama Makanan')
    restomakanandetail_ids = fields.One2many(comodel_name='resto.makanandetail', inverse_name='restomakanan_id', string='Bahan-bahan')
    harga = fields.Integer(string='Harga per Porsi')
    qty_jual = fields.Integer(string='Quantity Penjualan')
    
class RestoMakananDetail(models.Model):
    _name = 'resto.makanandetail'
    _description = 'RestoMakananDetail'
    restobahan_id = fields.Many2one(comodel_name='resto.bahan', string='Nama Bahan')
    kebutuhan = fields.Integer(string='Kebutuhan')
    restomakanan_id = fields.Many2one(comodel_name='resto.makanan', string='Makanan')
    
    
    

    
