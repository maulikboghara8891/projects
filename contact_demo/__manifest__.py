{
    "name": "Contact demo",
    'version': '19.0.1.0.0',
    'category': 'Website',
    'summary': 'Contact demo',
    'author': 'maulik',
    'license': 'LGPL-3',
    'description': """ contact demo""",
    'website': 'https://www.odoo.com',

    "depends": [
        'base','sale'
    ],
    "data": [
        # "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/sale_order.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
