from odoo import fields, models, api
import uuid

class IdApplication(models.Model):
    _name = 'id.application'
    _description = 'National Id Application'


    name = fields.Char('Applicant Full name', required=True)
    date_of_birth = fields.Date('Date of Birth', required=True)
    sex = fields.Selection([
            ('male', 'Male'),
            ('female', 'Female')
        ])
    country_of_origin = fields.Char('Country of Origin', required=True)
    parent_nin = fields.Char('Parent NIN')


    lc_letter = fields.Binary('LC Reference Letter', required=True)
    photo = fields.Binary('Applicant Photo', required=True)
    nin = fields.Char('National ID Number', readonly=True)
    stage = fields.Selection([
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved_stage1', 'Approved Stage 1'),
            ('appoved_stage2', 'Approved Stage 2'),
            ('rejected', 'Rejected'),
        ], default='draft', string='Status')


    def _generate_nin(self):
        '''
            Method to generate unique ID number
        '''
        uid = self.env['ir.sequence'].next_by_code('national.id.number')
        return uid

    @api.model
    def create(self, vals):
        ''' Override the create method to automatically generate National ID'''
        vals['nin'] = self._generate_nin()
        return super(IdApplication, self).create(vals)

    @api.constrains('date_of_birth')
    def _check_age(self):
        ''' Ensure the applicants are over 16 years'''
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                age = today.year - record.date_of_birth.year
                if age < 16:
                    raise ValidationError('Applicant must be at least 16 years')

