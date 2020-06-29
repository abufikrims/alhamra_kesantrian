#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class level_tahsin(models.Model):

    _name = "cdn.level_tahsin"
    _description = "Model untuk mencatat level Tahsin Santri "

    name = fields.Char( required=True, string="Name",  help="")
    keterangan = fields.Char( string="Keterangan",  help="")


