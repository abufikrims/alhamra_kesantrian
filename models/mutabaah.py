from odoo import models, fields, api, _

class mutabaah(models.Model):

    _name = "cdn.mutabaah"
    _description = "Master data Mutabaah"

    name = fields.Char( required=True, string="Name",  help="")
    kategori = fields.Selection(selection=[('disiplin','Kedisiplinan'),('adab','Adab'),('ibadah','Ibadah')],  string="Kategori",  help="")
    is_tampil = fields.Boolean(string="Ditampilkan ?", default=True)
    skor = fields.Integer(string='Skor/Nilai', default=1)
    
    

class mutabaah_harian(models.Model):

    _name = "cdn.mutabaah_harian"
    _description = "Data Mutabaah harian"

    name = fields.Char( readonly=True, default='Auto', string="No Referensi",  help="")
    tanggal = fields.Date( string="Tanggal", default=fields.Date.context_today, required=True, help="")
    kategori = fields.Selection(selection=[('disiplin','Kedisiplinan'),('adab','Adab'),('ibadah','Ibadah')],  string="Kategori",  help="")

    siswa_id = fields.Many2one(comodel_name="res.partner",  string="Siswa", required=True, domain=[('student', '=', True)], help="")
    halaqoh_id = fields.Many2one('cdn.halaqoh', 'Halaqoh', related='siswa_id.halaqoh_id', readonly=True)
    mutabaah_lines = fields.One2many(comodel_name="cdn.mutabaah_line",  inverse_name="mutabaah_id",  string="Mutabaah lines",  help="")

    _sql_constraints = [('mutabaah_harian_uniq', 'unique(tanggal, siswa_id, kategori)', 'Data Mutabaah Harian untuk Siswa tersebut sudah ada di tanggal tersebut !')]

    @api.onchange('kategori')
    def onchange_kategori(self):
        if self.kategori:
            nilai = []
            self.mutabaah_lines = [(5,0,0)]
            obj_mutabaah = self.env['cdn.mutabaah'].search([('kategori','=',self.kategori),('is_tampil','=',True)])
            for x in obj_mutabaah:
                nilai.append({'name': x.id, 'is_sudah': True, 'keterangan':'-'})

            data = {'mutabaah_lines': nilai}
            self.update(data)

    def btn_uncheckall(self):
        nilai = []
        self.mutabaah_lines = [(5,0,0)]
        obj_mutabaah = self.env['cdn.mutabaah'].search([('kategori','=',self.kategori),('is_tampil','=',True)])
        for x in obj_mutabaah:
            nilai.append({'name': x.id, 'is_sudah': False, 'keterangan':'-'})

        data = {'mutabaah_lines': nilai}
        self.update(data)
    
    def btn_checkall(self):
        nilai = []
        self.mutabaah_lines = [(5,0,0)]
        obj_mutabaah = self.env['cdn.mutabaah'].search([('kategori','=',self.kategori),('is_tampil','=',True)])
        for x in obj_mutabaah:
            nilai.append({'name': x.id, 'is_sudah': True, 'keterangan':'-'})

        data = {'mutabaah_lines': nilai}
        self.update(data)
        
        

    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.mutabaah_harian')
        return super(mutabaah_harian, self).create(vals)
    
   


class mutabaah_line(models.Model):

    _name = "cdn.mutabaah_line"
    _description = "Detail mutabaah harian"

    mutabaah_id = fields.Many2one('cdn.mutabaah_harian', 'Mutabaah Harian', required=True, ondelete='cascade')
    name = fields.Many2one(comodel_name="cdn.mutabaah",  string="Mutabaah",  help="")
    is_sudah = fields.Boolean( string="Dilakukan",  default=False, help="")
    keterangan = fields.Char( string="Keterangan",  help="")


class mutabaah_batch(models.TransientModel):
    _name = 'cdn.mutabaah_batch'
    _description = 'Batch Input untuk mutabaah harian'

    name = fields.Char(string='Nama Halaqoh')
    tanggal = fields.Date(string='Tanggal')
    state = fields.Selection(selection=[('draft','Draft'),('proses','Proses'),('done','Selesai')],  string="Status",  help="Klik Done - untuk membuat daftar Mutabaah Harian nya") 
    _sql_constraints = [('mutabaah_batch_uniq', 'unique(name, tanggal)', 'Data Mutabaah Harian untuk Halaqoh sudah ada di tanggal tersebut !')]



    

