from odoo import models, fields

class EmployeeSignTemplate(models.Model):
    _name = 'employee.sign.template'
    _description = 'Employee Sign Template'

    name = fields.Char(string="Template Name", required=True)
    document = fields.Binary(string="Document")
    document_name = fields.Char(string="Document Name")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
    ], string="Status", default='draft')