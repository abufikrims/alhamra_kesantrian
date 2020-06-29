#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class tahfidz_hadits(models.Model):

    _name = "cdn.tahfidz_hadits"
    _description = "Model untuk mencatat aktivitas tahfidz hadits "

    name = fields.Char( readonly=True, default='Auto', string="No Referensi",  help="")
    tanggal = fields.Date( string="Tanggal", default=fields.Date.context_today, required=True, help="")
    nilai = fields.Integer( string="Nilai",  help="")
    keterangan = fields.Char( string="Keterangan",  help="")
    state = fields.Selection(selection=[('draft','Draft'),('done','Done')],  string="State",  help="")


    hadits_id = fields.Many2one(comodel_name="cdn.hadits",  string="Hadits",  help="")
    siswa_id = fields.Many2one(comodel_name="res.partner",  string="Siswa", required=True, domain=[('student', '=', True)],  help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)
    guru_id = fields.Many2one(comodel_name="hr.employee",  string="Guru",  help="")
    nilai_id = fields.Many2one(comodel_name="cdn.nilai_tahfidz",  string="Nilai",  help="")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.tahfidz_hadits')
        return super(tahfidz_hadits, self).create(vals)
