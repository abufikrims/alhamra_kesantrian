from datetime import date
from odoo import api, fields, models,_
from odoo.exceptions import UserError

from odoo import api, fields, models


class company_inherit(models.Model):
    _inherit = 'res.company'

    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Tahun Ajaran')

class perijinan(models.Model):
    _name = 'cdn.perijinan'
    _inherit = 'mail.thread'
    _description = 'Data Perijinan Santri'

    name = fields.Char(string="No. Referensi",  help="", readonly=True, default='Auto')
    tgl_ijin = fields.Date( string="Tanggal Ijin", default=fields.Date.context_today, required=True, help="")
    tgl_hrs_kembali = fields.Date( string="Tanggal kembali", required=True,  help="")
    lama_ijin = fields.Integer('Lama Ijin', readonly=True, compute='compute_day',  store=True)
    state = fields.Selection(selection=[('Draft','Pengajuan'),('Check','Diperiksa'),('Approved','Disetujui'),('Rejected','Ditolak'),('Permission','Ijin Keluar'),('Return','Kembali')],  string="State", default="Draft", help="", track_visibility="always")
    penjemput = fields.Char( string="Penjemput",  help="")
    keperluan = fields.Text( string="Keperluan",  help="")
    tgl_kembali = fields.Date( string="Tanggal Masuk",  help="")
    jam_kembali = fields.Char(string="Jam Kembali", help="")
    waktu_keluar = fields.Datetime(string="Keluar Pondok", readonly=True)
    waktu_kembali = fields.Datetime(string="Kembali ke Pondok", readonly=True)
    catatan = fields.Text( string="Catatan",  help="")


    siswa_id = fields.Many2one(comodel_name="res.partner",  string="Siswa", required=True, domain=[('student', '=', True)], help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.perijinan')
        return super(perijinan, self).create(vals)

    @api.multi
    def action_confirm(self):
        return self.write({'state': 'Draft'})

    def action_checked(self):
        return self.write({'state': 'Check'})


    def action_approved(self):
        return self.write({'state': 'Approved'})

    def action_rejected(self):
        return self.write({'state': 'Rejected'}) 

    def action_permission(self):
        return self.write({'state': 'Permission'}) 


    @api.one
    @api.depends('tgl_ijin', 'tgl_hrs_kembali')
    def compute_day(self):
        if self.tgl_ijin and self.tgl_hrs_kembali:
            tgl_ijin = fields.Datetime.from_string(self.tgl_ijin)
            tgl_hrs_kembali = fields.Datetime.from_string(self.tgl_hrs_kembali)
            self.lama_ijin = abs((tgl_hrs_kembali - tgl_ijin).days) + 1


class pelanggaran(models.Model):

    _name = "cdn.pelanggaran"
    _description = 'Model untuk Mencatat Aktivitas Pelanggaran'
    name = fields.Char(string="No. Referensi",  help="", readonly=True, default='Auto')
    tgl_pelanggaran = fields.Date( string="Tanggal pelanggaran", default=fields.Date.context_today, help="")
    #diperiksa_oleh = fields.Char( string="Diperiksa oleh",  help="")
    diperiksa_oleh = fields.Many2one('res.users', 'Diperiksa oleh', required=True, default=lambda self: self.env.user)
    poin = fields.Integer( string="Poin",  help="")
    deskripsi = fields.Text( string="Deskripsi",  help="")


    tindakan_id = fields.Many2one(comodel_name="cdn.tindakan_hukuman",  string="Tindakan",  help="")
    siswa_id = fields.Many2one(comodel_name="res.partner", required=True, string="Siswa", domain=[('student', '=', True)], help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.pelanggaran')
        return super(pelanggaran, self).create(vals)

class tindakan_hukuman(models.Model):

    _name = "cdn.tindakan_hukuman"
    _description = 'Model untuk Jenis Tindakan Hukuman'
    name = fields.Char( required=True, string="Name",  help="")
    poin = fields.Integer( string="Poin",  help="")
    level_pelanggaran = fields.Selection(selection=[('Ringan','Ringan'),('Sedang','Sedang'),('Berat','Berat'),('Dikeluarkan','Dikeluarkan')],  string="Level pelanggaran",  help="")
    deskripsi = fields.Text( string="Deskripsi",  help="")

class kesehatan(models.Model):

    _name = "cdn.kesehatan"
    _description = 'Model untuk Aktivitas Kesehatan Santri'
    name = fields.Char( required=True, string="Name", readonly=True, help="", default="Auto")
    tgl_periksa = fields.Date( string="Tanggal Periksa", default=fields.Date.context_today, required=True, help="", copy=False)
    keluhan = fields.Text( string="Keluhan", required=True,  help="")
    diagnosa = fields.Text( string="Diagnosa", help="")
    obat = fields.Text( string="Obat",  help="")
    diperiksa_oleh = fields.Char( string="Diperiksa oleh",  help="")
    state   = fields.Selection(selection=[('Periksa','Periksa'),('Pengobatan','Pengobatan'),('Rawat','Rawat'),('Sembuh','Sembuh')],  string="Kondisi", help="", copy=False)
    tgl_selesai = fields.Date( string="Tanggal Selesai", readonly=True, help="")
    catatan = fields.Text( string="Catatan",  help="")
    lokasi_rawat =  fields.Selection(string='Dirawat di', selection=[('uks', 'UKS'), ('rumah sakit', 'Rumah Sakit'),('rumah','Pulang ke Rumah')], copy=False)
    keterangan_rawat =  fields.Char(string='Keterangan Perawatan')
    
    


    siswa_id = fields.Many2one(comodel_name="res.partner", required=True,  string="Siswa",  domain=[('student', '=', True)],  help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.kesehatan')
        return super(kesehatan, self).create(vals)

    @api.multi
    def kesehatan_confirm(self):
        return self.write({'state': 'Periksa'})

    @api.multi
    def action_pengobatan(self):
        return self.write({'state':'Pengobatan'})

    def action_rawat(self):
        return self.write({'state':'Rawat'})

    def action_sembuh(self):
       self.tgl_selesai = date.today()
       return self.write({'state':'Sembuh'})

class prestasi_siswa(models.Model):

    _name = "cdn.prestasi_siswa"
    _description = 'Model untuk Mencatat Prestasi Santri'
    name = fields.Char( string="No. Referensi", readonly=True, help="", default="Auto")
    tgl_prestasi = fields.Date( string="Tanggal prestasi", default=fields.Date.context_today, required=True, help="")
    tingkat_prestasi = fields.Selection(selection=[('Internal','Internal'),('Lokal','Lokal'),('Kecamatan','Kecamatan'),('Kota','Kota'),('Propinsi','Propinsi'),('Nasional','Nasional'),('Internasional','Internasional')],  string="Tingkat prestasi",  help="")
    juara_ke = fields.Char( string="Juara ke",  help="")
    jns_prestasi_id = fields.Many2one(comodel_name="cdn.jns_prestasi",  string="Jenis prestasi",  help="")
    siswa_id = fields.Many2one(comodel_name="res.partner", required=True,  string="Siswa", domain=[('student', '=', True)],  help="")
    keterangan =  fields.Text(string='Keterangan')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.prestasi_siswa')
        return super(prestasi_siswa, self).create(vals)

class jns_prestasi(models.Model):

    _name = "cdn.jns_prestasi"
    _description = 'Model untuk Mencatat Jenis Prestasi'
    name = fields.Char( required=True, string="Name",  help="")
    deskripsi = fields.Text( string="Deskripsi",  help="")

class lokasi_fasilitas(models.Model):
    _name = "cdn.lokasi_fasilitas"
    _description = "Model untuk mencatat daftar fasilitas pesantren "

    name = fields.Char(string='Nama Fasilitas')
    parent_id = fields.Many2one(comodel_name='cdn.lokasi_fasilitas', string='Lokasi Induk', index=True, ondelete='cascade')
    child_ids = fields.One2many(comodel_name='cdn.lokasi_fasilitas', inverse_name='parent_id', string='Detail')
    
    jns_fasilitas = fields.Selection(string='Jenis Fasilitas', selection=[('kelas', 'Ruang Kelas'), ('asrama', 'Asrama'), ('kantor', 'Kantor'), ('lab', 'Laboratorium'), ('lapangan', 'Lapangan'), ('lainnya', 'Lainnya'),  ])
    is_kamar_santri =  fields.Boolean(string='Kamar Santri ?', domain=[('jns_fasilitas','=','asrama')])

    

    @api.multi
    def name_get(self):
        ret_list = []
        for location in self:
            orig_location = location
            name = location.name
            while location.parent_id:
                location = location.parent_id
                if not name:
                    raise UserError(_('You have to set a name for this location'))
                name = location.name + "/" + name
            ret_list.append((orig_location.id, name))
        return ret_list

class pembagian_kamar(models.Model):
    _name = "cdn.kamar"
    _description = "Model untuk mencatat pembagian kamar"
    _rec_name = 'kamar_id'

    kamar_id = fields.Many2one(comodel_name='cdn.lokasi_fasilitas', string='Nama Kamar', domain=[('jns_fasilitas','=','asrama'),('is_kamar_santri','=', True)])
    parent_id = fields.Many2one(comodel_name='cdn.lokasi_fasilitas', string='Lokasi', related='kamar_id.parent_id')
    
    musyrif_id = fields.Many2one(comodel_name='hr.employee', string='Musyrif/Pembina')
    siswa_ids = fields.Many2many('res.partner', 'siswa_kamar', 'siswa_id', 'partner_id', 'Siswa', domain=[('student', '=', True)])

    _sql_constraints = [('kamar_uniq', 'unique(kamar_id)', 'Identitas Kamar Santri sudah ada !')]


    @api.one
    def update_room(self):
        #obj_invoice = self.env['account.invoice']

        #iid = obj_invoice.search([('partner_id', 'in', [i.id for i in self.siswa_ids])])
        #if iid:
        #    iid.write({'class_id': self.name.id})

        for x in self.siswa_ids:
            x.write({'fasilitas_id': self.kamar_id.id})
        return True
    
# class siswa_kamar(models.Model):
#     _inherit = "res.partner"

    
    
class siswa_kamar(models.Model):
    _inherit = "res.partner"

    fasilitas_id = fields.Many2one(comodel_name='cdn.lokasi_fasilitas', string='Kamar Santri', readonly=True)
    tahfidz_surah = fields.Char(string='Tahfidz Surah', readonly=True)
    halaqoh_id = fields.Many2one(comodel_name='cdn.halaqoh', string='Halaqoh', readonly=True)
    
    
    @api.multi
    def open_perijinan(self):
        return {
            'name'  : _('Perijinan'),
            'domain' : [('siswa_id','=',self.id)],
            'view_type' : 'form',
            'res_model' : 'cdn.perijinan',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }  

    def get_perijinan_count(self):
        count = self.env['cdn.perijinan'].search_count([('siswa_id','=', self.id)])
        self.perijinan_count = count

    def open_kesehatan(self):
        return {
            'name'  : _('Kesehatan'),
            'domain' : [('siswa_id','=',self.id)],
            'view_type' : 'form',
            'res_model' : 'cdn.kesehatan',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }

    def get_kesehatan_count(self):
        count = self.env['cdn.kesehatan'].search_count([('siswa_id','=', self.id)])
        self.kesehatan_count = count 
    

    def open_pelanggaran(self):
        return {
            'name'  : _('Pelanggaran'),
            'domain' : [('siswa_id','=',self.id)],
            'view_type' : 'form',
            'res_model' : 'cdn.pelanggaran',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }

    def get_pelanggaran_count(self):
        count = self.env['cdn.pelanggaran'].search_count([('siswa_id','=', self.id)])
        self.pelanggaran_count = count  

    perijinan_count = fields.Integer(string='Perijinan', compute='get_perijinan_count')
    kesehatan_count = fields.Integer(string='Kesehatan', compute='get_kesehatan_count')
    pelanggaran_count = fields.Integer(string='Pelanggaran', compute='get_pelanggaran_count')

    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('nis',operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()


        # args = args or []
        # if name:
        #     recs = self.search([
        #         '|',
        #         ('name', operator, name),
        #         ('nis', operator, name)
        #     ] + args, limit=limit)
        # else:
        #     recs = self.search([] + args, limit=limit)
        # return recs.name_get()



    
    
    