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
            i_partner.write({'tahfidz_surah': record.surah_id.name+' # '+str(record.ayat_awal)+' - '+str(record.ayat_akhir)+' # '+str(record.jml_baris)+' baris # Nilai: '+str(record.nilai)})
            # '+str(self.ayat_awal)+' - '+str(self.ayat_akhir)})
        return record

    def write(self,values):
        i_partner = self.env['res.partner'].search([('id', '=', self.siswa_id.id)])
        if i_partner:
            i_partner.write({'tahfidz_surah': self.surah_id.name+' # '+str(self.ayat_awal)+' - '+str(self.ayat_akhir)+' # '+str(self.jml_baris)+' baris # Nilai: '+str(self.nilai)})
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

    name = fields.Char( required=True, string="No Referensi",  help="")
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

    

    
