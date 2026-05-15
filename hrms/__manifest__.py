{
    "name": "HR Management",
    'version': '19.0.1.0.0',
    'category': 'Website',
    'summary': 'hr manage',
    'author': 'maulik',
    'license': 'LGPL-3',
    'description': """hr""",
    'website': 'https://www.odoo.com',

    "depends": [
        'base'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/employee_view.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
