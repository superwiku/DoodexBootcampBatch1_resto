from odoo import models, fields, api, _

class RestoMember(models.Model):
    _inherit = 'res.partner'
    _description = 'model.technical.name'      

    is_member = fields.Boolean(string='Member ?', default=True)
    referensi = fields.Char(
        string="No. Member",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))  

    @api.model
    def create(self, vals):
        if vals.get('referensi', _('New')) == _('New'):
            vals['referensi'] = self.env['ir.sequence'].next_by_code('wikuresto.referensi.member') or _('New')
        record = super(RestoMember, self).create(vals)
        return record      
