#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields,exceptions, api, _

class tahsin(models.Model):

    _name = "cdn.tahsin"
    _description = "Model untuk mencatat Aktivitas Tahsin "

    name = fields.Char( readonly=True, default='Auto', string="No Referensi",  help="")
    tanggal = fields.Date( string="Tanggal", default=fields.Date.context_today, required=True, help="")
    nilai = fields.Integer( string="Nilai Makhroj",  help="Isikan dengan nilai angka 0-100")
    nilai2 = fields.Integer(string='Nilai Tajwid', help='Isikan dengan nilai angka 0-100')
    nilai3 = fields.Integer(string='Mad', help='Isikan dengan nilai angka 0-100')
    halaman = fields.Integer(string='Halaman')
    
    
    keterangan = fields.Char( string="Keterangan",  help="")
    state = fields.Selection(selection=[('draft','Draft'),('done','Done')],  string="State",  help="")


    siswa_id = fields.Many2one(comodel_name="res.partner",  string="Siswa", required=True, domain=[('student', '=', True)],  help="")
    kelas_id = fields.Many2one('master.kelas', 'Kelas', related='siswa_id.class_id', readonly=True)
    halaqoh_id = fields.Many2one('cdn.halaqoh', 'Halaqoh', related='siswa_id.halaqoh_id', readonly=True)
    ustadz_id = fields.Many2one('hr.employee', string='Ustadz Pembimbing', default=lambda self: self.env.user)
    #guru_id = fields.Many2one(comodel_name="hr.employee",  string="Guru",  help="")
    level_id = fields.Many2one(comodel_name="cdn.level_tahsin",  string="Level",  help="")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cdn.tahsin')
        return super(tahsin, self).create(vals)

    @api.multi
    def write(self,values):
        res = super(tahsin,self).write(values)
        if (not self.level_id) or (self.nilai<=0) or (self.nilai2<=0) or (self.nilai3<=0):
            raise exceptions.ValidationError('ERROR ! Periksa kembali pengisian Jilid Tahsin, dan Nilai-nilai Tahsin !')
        
        # i_partner = self.env['res.partner'].search([('id', '=', self.siswa_id.id)])
        # if i_partner:
        #     i_partner.write({'tahfidz_surah': str(self.surah_id.name)+' # '+str(self.ayat_awal)+' - '+str(self.ayat_akhir)+' # '+str(self.jml_baris)+' baris # '+str(self.nilai_id.name)})
        return res

    @api.multi
    def action_confirm(self):
        if (not self.level_id) or (self.nilai<=0) or (self.nilai2<=0) or (self.nilai3<=0):
            raise exceptions.ValidationError('Proses KONFIRMASI harus menyertakan Keterangan Jilid Tahsin dan Nilai-nilainya !')
        return self.write({'state': 'done'})
    
    @api.multi
    def action_draft(self):
        return self.write({'state': 'draft'})

class absen_tahsin(models.Model):
    _name = 'cdn.absen_tahsin'
    _description = 'Mencatat absensi proses tahsin'

    name = fields.Date('Tanggal', required=True, default=fields.Date.context_today)

    def _default_fiscalyear(self):
        return self.env['res.company'].search([('id','=',1)]).fiscalyear_id

    state = fields.Selection(selection=[('draft','Draft'),('proses','Proses'),('done','Selesai')],  string="Status",  help="Klik Done - untuk membuat daftar absensi Tahsin dan aktivitas nya") 
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Tahun Ajaran',  default=_default_fiscalyear)
    halaqoh_id = fields.Many2one('cdn.halaqoh', 'Nama Halaqoh', required=True, domain="[('fiscalyear_id', '=', fiscalyear_id)]")
    ustadz_halaqoh = fields.Many2one('hr.employee', string='Ustadz Pembimbing', related='halaqoh_id.ustadz_halaqoh', readonly=True)
     
    absen_tahsin_line = fields.One2many('absen_tahsin.line', 'absen_line_id', 'Daftar Kehadiran')

    _sql_constraints = [('absen_tahsin_uniq', 'unique(name,  halaqoh_id, fiscalyear_id)', 'Data harus unik !')]

    @api.onchange('halaqoh_id')
    def onchange_halaqoh_id(self):
        if self.halaqoh_id:

            siswa = []
            
            for x in self.halaqoh_id.siswa_ids:
                siswa.append({'name': x.id, 'kehadiran': 'hadir'})

            data = {'absen_tahsin_line': siswa}
            self.update(data)

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super(absen_tahsin,self).create(vals)

    @api.multi
    def action_confirm(self):
        return self.write({'state': 'done'})
    
    @api.multi
    def action_proses(self):
        # obj_tahfidz_quran = self.env['cdn.sesi_tahfidz']
        obj_tahsin = self.env['cdn.tahsin']
        for x in self.absen_tahsin_line:
            # Catat yang hadir saja
            if x.kehadiran=='hadir':
                obj_tahsin.create({
                    'tanggal'   : self.name, 
                    'siswa_id'  : x.name.id,
                    'ustadz_id' : self.ustadz_halaqoh.id,
                    'state': 'draft'
                
                })
            

        return self.write({'state': 'proses'})

    

class absen_tahsin_line(models.Model):
    _name = 'absen_tahsin.line'

    absen_line_id = fields.Many2one('cdn.absen_tahsin', 'Penilaian Kehadiran', required=True, ondelete='cascade')
    name = fields.Many2one('res.partner', 'Siswa', required=True, domain=[('student', '=', True)])
    nis = fields.Char(string='NIS', related='name.nis')
    kehadiran = fields.Selection(string='Kehadiran', selection=[('hadir', 'Hadir'), ('sakit', 'Sakit'),  ('ijin', 'Ijin'),  ('alpa', 'Alpa'), ])

    
