#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _

class tahfidz_quran(models.Model):

    _name = "cdn.tahfidz_quran"
    _description = "Model untuk mencatat aktivitas tahfidz Al Quran "

    name = fields.Char( readonly=True, default='Auto', string="No Referensi",  help="")
    tanggal = fields.Date( string="Tanggal", default=fields.Date.context_today, required=True, help="")
    nilai = fields.Integer( string="Nilai",  help="")
    keterangan = fields.Char( string="Keterangan",  help="")
    state = fields.Selection(selection=[('draft','Draft'),('done','Done')],  string="State",  help="")


    siswa_id = fields.Many2one(comodel_name="res.partner",  string="Siswa", required=True, domain=[('student', '=', True)], help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)
    halaqoh_id = fields.Many2one('cdn.halaqoh', 'Halaqoh', related='siswa_id.halaqoh_id', readonly=True)
    last_tahfidz = fields.Char(string="Tahfidz Terakhir", related="siswa_id.tahfidz_surah")
    #class_id = fields.Char(string="Kelas", related="siswa_id.class_id")
    surah_id = fields.Many2one(comodel_name="cdn.quran",  string="Surah",  help="")
    jml_ayat = fields.Integer(string="Jumlah Ayat", related="surah_id.jml_ayat")
    ayat_awal = fields.Integer(string="Ayat Awal", help="")
    ayat_akhir = fields.Integer(string="Ayat Akhir", help="")

    halaman = fields.Integer(string="Halaman", help="")
    jml_baris = fields.Integer(string="Jumlah Baris", help="")
    sesi_tahfidz_id = fields.Many2one(comodel_name='cdn.sesi_tahfidz', string='Sesi Tahfidz')
    
    guru_id = fields.Many2one('res.users', 'Guru', required=True, default=lambda self: self.env.user)
    nilai_id = fields.Many2one(comodel_name="cdn.nilai_tahfidz",  string="Kategori",  help="")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.tahfidz_quran')
        record = super(tahfidz_quran, self).create(vals)
        i_partner = self.env['res.partner'].search([('id', '=', vals['siswa_id'])])
        if i_partner:
            i_partner.write({'tahfidz_surah': record.surah_id.name+' # '+str(record.ayat_awal)+' - '+str(record.ayat_akhir)+' # '+str(record.jml_baris)+' baris # '+record.nilai_id.name})
            # '+str(self.ayat_awal)+' - '+str(self.ayat_akhir)})
        return record

    def write(self,values):
        i_partner = self.env['res.partner'].search([('id', '=', self.siswa_id.id)])
        if i_partner:
            i_partner.write({'tahfidz_surah': self.surah_id.name+' # '+str(self.ayat_awal)+' - '+str(self.ayat_akhir)+' # '+str(self.jml_baris)+' baris # '+self.nilai_id.name})
        return super(tahfidz_quran,self).write(values)

    @api.constrains('ayat_awal','ayat_akhir','jml_ayat')
    def _check_ayat(self):
        if self.ayat_awal>self.ayat_akhir or self.ayat_awal>self.jml_ayat or self.ayat_akhir>self.jml_ayat:
            raise exceptions.ValidationError('Penulisan Ayat Awal dan Ayat Akhir Salah ! Tidak boleh melebihi Jumlah Ayat dalam Surah tsb !')
    

class sesi_tahfidz(models.Model):

    _name = "cdn.sesi_tahfidz"
    _description = 'Model untuk Sesi Tahfidz'
    name = fields.Char( required=True, string="Nama Sesi",  help="")
    keterangan = fields.Char(string="Keterangan")
    
class halaqoh(models.Model):
    _name = "cdn.halaqoh"
    _description = "Model untuk Pembagian Kelas Halaqoh"

    name = fields.Char( required=True, string="Nama Halaqoh",  help="")
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Tahun Ajaran', required=True)
    ustadz_halaqoh = fields.Many2one(comodel_name='hr.employee', string='Ustadz Pembimbing')
    # siswa_ids = fields.One2many(comodel_name='cdn.halaqoh_lines', inverse_name='', string='Siswa')
    siswa_ids = fields.Many2many('res.partner', 'siswa_halaqoh', 'siswa_id', 'partner_id', 'Siswa', domain=[('student', '=', True)])
    keterangan = fields.Char(string="Keterangan")

    _sql_constraints = [('halaqoh_uniq', 'unique(name, fiscalyear_id)', 'Halaqah tersebut sudah ada !')]

    @api.one
    def update_halaqoh(self):
        for x in self.siswa_ids:
            x.write({'halaqoh_id': self.id})
        return True

class absen_quran(models.Model):
    _name = "cdn.absen_quran"
    _description = "Model untuk Absensi Halaqoh Quran"

    name = fields.Date('Tanggal', required=True, default=fields.Date.context_today)

    def _default_fiscalyear(self):
        return self.env['res.company'].search([('id','=',1)]).fiscalyear_id

    #fiscalyear_id = fields.Many2one('account.fiscalyear', 'Tahun Ajaran', required=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Tahun Ajaran',  default=_default_fiscalyear)
    halaqoh_id = fields.Many2one('cdn.halaqoh', 'Nama Halaqoh', required=True, domain="[('fiscalyear_id', '=', fiscalyear_id)]")
    sesi_id = fields.Many2one('cdn.sesi_tahfidz', 'Sesi Tahfidz', required=True)
    absen_quran_line = fields.One2many('absen_quran.line', 'absen_line_id', 'Daftar Kehadiran')

    _sql_constraints = [('absen_quran_uniq', 'unique(name, sesi_id, halaqoh_id, fiscalyear_id)', 'Data harus unik !')]

    @api.onchange('halaqoh_id')
    def onchange_halaqoh_id(self):
        if self.halaqoh_id:

            siswa = []
            for x in self.halaqoh_id.siswa_ids:
                siswa.append({'name': x.id, 'kehadiran': 'hadir'})

            data = {'absen_quran_line': siswa}
            self.update(data)

class absen_quran_line(models.Model):
    _name = 'absen_quran.line'

    absen_line_id = fields.Many2one('cdn.absen_quran', 'Penilaian Kehadiran', required=True, ondelete='cascade')
    name = fields.Many2one('res.partner', 'Siswa', required=True, domain=[('student', '=', True)])
    nis = fields.Char(string='NIS', related='name.nis')
    kehadiran = fields.Selection(string='Kehadiran', selection=[('hadir', 'Hadir'), ('sakit', 'Sakit'),  ('ijin', 'Ijin'),  ('alpa', 'Alpa'), ])
    


    

    

    
