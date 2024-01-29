from odoo import models, fields, api, _
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None

from io import BytesIO

from odoo.exceptions import ValidationError, UserError


class RestoPenjualan(models.Model):
    _name = 'resto.penjualan'
    _description = 'RestoPenjualan'
    _rec_name = 'kode_penjualan'
    
    qr_code = fields.Char(compute='_compute_qr_code', string='QR Code', store = True)    
    kode_penjualan = fields.Char(string="Kode Penjualan", required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    nama = fields.Char(string='Nama Pembeli')
    membership = fields.Boolean(string='Apakah member ?', default = False)    
    tgl_transaksi = fields.Datetime(string='Tanggal Transaksi', default=fields.Datetime.now())
    total_bayar = fields.Integer(compute='_compute_total_bayar', string='Total Bayar', store=True)
    restodetailpenjualanmakanan_ids = fields.One2many(comodel_name='resto.detailpenjualanmakanan', inverse_name='restopenjualanmakanan_id', string='Detail Penjualan Makanan')
    restodetailpenjualanminuman_ids = fields.One2many(comodel_name='resto.detailpenjualanminuman', inverse_name='restopenjualanminuman_id', string='Detail Penjualan Minuman')
    
    @api.depends('kode_penjualan')
    def _compute_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
                qr.add_data(rec.kode_penjualan)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
    
    @api.depends('restodetailpenjualanmakanan_ids','restodetailpenjualanminuman_ids')
    def _compute_total_bayar(self):
        for rec in self:
            a = self.env['resto.detailpenjualanmakanan'].search([('restopenjualanmakanan_id','=',rec.id)]).mapped('subtotal')   
            b = self.env['resto.detailpenjualanminuman'].search([('restopenjualanminuman_id','=',rec.id)]).mapped('subtotal')        
            total = sum(a) + sum(b)
            rec.total_bayar = total

    @api.model
    def create(self,vals):        
        if vals.get('kode_penjualan', _("New")) == _("New"):   
            membership = vals.get('membership',False)
            if membership == True:            
                vals['kode_penjualan'] = self.env['ir.sequence'].next_by_code('wikuresto.referensi.penjualan_member') or _("New")    
            else:
                vals['kode_penjualan'] = self.env['ir.sequence'].next_by_code('wikuresto.referensi.penjualan_nonmember') or _("New")
        record = super(RestoPenjualan, self).create(vals)
        return record

class RestoDetailPenjualanMakanan(models.Model):
    _name = 'resto.detailpenjualanmakanan'
    _description = 'DetailPenjualanMakanan'
    _rec_name = 'restomakanan_id'

    restomakanan_id = fields.Many2one(comodel_name='resto.makanan', string='Nama Makanan')
    restopenjualanmakanan_id = fields.Many2one(comodel_name='resto.penjualan', string='Penjualan Makanan')
    
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Sub Total')
    
    @api.depends('restomakanan_id','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.restomakanan_id.harga    
    
    @api.model
    def create(self, vals):    
        record = super(RestoDetailPenjualanMakanan, self).create(vals)   
        a = self.env['resto.makanan'].search([('id','=',record.restomakanan_id.id)]).mapped('restomakanandetail_ids')   
        for rec in a:
            self.env['resto.bahan'].search([('id','=',rec.restobahan_id.id)]).write({'stok': rec.restobahan_id.stok - (rec.kebutuhan * record.qty)})
        return record


class RestoDetailPenjualanMinuman(models.Model):
    _name = 'resto.detailpenjualanminuman'
    _description = 'RestoDetailPenjualanMinuman'
    _rec_name = 'restominuman_id'
    
    restominuman_id = fields.Many2one(comodel_name='resto.minuman', string='Nama Minuman')
    restopenjualanminuman_id = fields.Many2one(comodel_name='resto.penjualan', string='Penjualan Minuman')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Sub Total')
    
    @api.depends('restominuman_id','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.restominuman_id.harga

    @api.model
    def create(self, vals):    
        record = super(RestoDetailPenjualanMinuman, self).create(vals)   
        a = self.env['resto.minuman'].search([('id','=',record.restominuman_id.id)]).mapped('restominumandetail_ids')   
        for rec in a:
            self.env['resto.bahan'].search([('id','=',rec.restobahan_id.id)]).write({'stok': rec.restobahan_id.stok - (rec.kebutuhan * record.qty)})
        return record