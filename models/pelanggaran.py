from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ref_pelanggaran(models.Model):
    _name           = 'ref.pelanggaran'
    _description    = 'Master / Referensi Data Pelanggaran'

    name            = fields.Char(string='Nama Pelanggaran', required=True, index=True)
    jns_pelanggaran_id = fields.Many2one(comodel_name='ref.jns_pelanggaran', string='Jenis Pelanggaran')
    kategori        = fields.Selection(string='Kategori', selection=[('Ringan', 'Ringan'), ('Sedang', 'Sedang'),('Berat', 'Berat'), ('Dikeluarkan', 'Sangat Berat'),])
    poin            = fields.Integer(string='Poin Pelanggaran')

class jenis_pelanggaran(models.Model):
    _name           = 'ref.jns_pelanggaran'
    _description    = 'Master Jenis/Kelompok Pelanggaran'

    name            = fields.Char(string='Jenis Pelanggaran')
    keterangan      = fields.Char(string='Keterangan')
    pelanggaran_ids = fields.One2many(comodel_name='ref.pelanggaran', inverse_name='jns_pelanggaran_id', string='')
    
    
    active          = fields.Boolean(string='Active', default=True)
    

    

