#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

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
    #class_id = fields.Char(string="Kelas", related="siswa_id.class_id")
    surah_id = fields.Many2one(comodel_name="cdn.quran",  string="Surah",  help="")
    jml_ayat = fields.Integer(string="Jumlah Ayat", related="surah_id.jml_ayat")
    ayat_ke = fields.Integer(string="Ayat ke", help="")
    halaman = fields.Integer(string="Halaman", help="")

    
    guru_id = fields.Many2one(comodel_name="hr.employee",  string="Guru",  help="")
    nilai_id = fields.Many2one(comodel_name="cdn.nilai_tahfidz",  string="Kategori",  help="")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.tahfidz_quran')
        return super(tahfidz_quran, self).create(vals)
