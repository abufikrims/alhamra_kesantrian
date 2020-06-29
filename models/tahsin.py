#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class tahsin(models.Model):

    _name = "cdn.tahsin"
    _description = "Model untuk mencatat Aktivitas Tahsin "

    name = fields.Char( readonly=True, default='Auto', string="No Referensi",  help="")
    tanggal = fields.Date( string="Tanggal", default=fields.Date.context_today, required=True, help="")
    nilai = fields.Integer( string="Nilai",  help="")
    keterangan = fields.Char( string="Keterangan",  help="")


    siswa_id = fields.Many2one(comodel_name="res.partner",  string="Siswa", required=True, domain=[('student', '=', True)],  help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)
    guru_id = fields.Many2one(comodel_name="hr.employee",  string="Guru",  help="")
    level_id = fields.Many2one(comodel_name="cdn.level_tahsin",  string="Level",  help="")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.tahsin')
        return super(tahsin, self).create(vals)
