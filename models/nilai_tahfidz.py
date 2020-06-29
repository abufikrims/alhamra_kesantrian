#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class nilai_tahfidz(models.Model):

    _name = "cdn.nilai_tahfidz"
    _description = "Model untuk mencatat Grade Nilai Tahfidz "

    name = fields.Char( required=True, string="Kategori Nilai",  help="")
    lulus = fields.Boolean( string="Lulus",  help="")


