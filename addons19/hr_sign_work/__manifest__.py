{
    'name': 'Sign-Work',
    'version': '1.0',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'author': 'Your Name',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/sign_template_views.xml',
        'views/menu.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}