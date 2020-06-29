#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class hadits(models.Model):

    _name = "cdn.hadits"
    _description = "Model untuk mencatat daftar Hafalan Hadits "

    name = fields.Char( required=True, string="Nama Hadits",  help="")
    kode = fields.Integer( string="Kode",  help="")
    no_hadits = fields.Char( string="No hadits",  help="")
    keterangan = fields.Char( string="Keterangan",  help="")
    matan_hadits = fields.Text( string="Matan hadits",  help="")


