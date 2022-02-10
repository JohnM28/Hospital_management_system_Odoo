from odoo import models, fields, api

class Log(models.Model):
    _name = 'hms.log'

    created_by = fields.Char()
    date = fields.Date()
    description = fields.Text()

    patient_ids = fields.Many2one('hms.patient')
