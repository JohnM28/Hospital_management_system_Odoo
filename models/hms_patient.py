from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError,UserError

class Hms(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birthdate = fields.Date()
    history = fields.Char()
    cr_ratio = fields.Float()
    blood_type = fields.Selection(string='Type', selection=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    pcr = fields.Boolean()
    avatar = fields.Image()
    address = fields.Text()
    age = fields.Integer()
    email = fields.Char(required=True)

    dep_id = fields.Many2one('hms.department')
    capacity = fields.Integer(related='dep_id.capacity')
    doctor_ids = fields.Many2many('hms.doctors')

    log_id = fields.One2many('hms.log','patient_ids')
    created_by = fields.Char(related='log_id.created_by')
    date = fields.Date(related='log_id.date')
    description = fields.Text(related='log_id.description')

    state = fields.Selection([
        ('underdetermined', 'underdetermined'),
        ('good', 'good'),
        ('fair', 'fair'),
        ('serious', 'serious'),
    ], default='underdetermined')


    def creat_log(self):
        log = self.env['hms.log'].create({
            'created_by': self.first_name,
            'date': date.today(),
            'description': self.state,
            'patient_ids': self.id,
        })


    def next_stage(self):
        if self.state == 'underdetermined':
            self.state = 'good'
            self.creat_log()

        elif self.state == 'good':
            self.state = 'fair'
            self.creat_log()

        elif self.state == 'fair':
            self.state = 'serious'
            self.creat_log()


    @api.onchange('birthdate')
    def _onchange_birthdate(self):
        if self.birthdate:
            self.age = date.today().year - self.birthdate.year

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR IS CHECKED',
                }
            }
        else:
            self.pcr = False

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail')