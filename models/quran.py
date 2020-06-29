#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class quran(models.Model):

    _name = "cdn.quran"
    _description = "Model untuk mencatat daftar Surah dlm Al Quran "
    

    name = fields.Char( required=True, string="Nama Surah",  help="")
    surah_ke = fields.Integer( string="Surah ke",  help="")
    jml_ayat = fields.Integer( string="Jumlah Ayat",  help="")
    terjemah = fields.Char( string="Arti",  help="")
    juz = fields.Integer( string="Juz",  help="")

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s . %s' % (rec.surah_ke, rec.name)))
        return res


