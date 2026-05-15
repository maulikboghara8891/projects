{
    "name": "inventory entp",
    'version': '19.0.1.0.0',
    'category': 'Website',
    'summary': 'inventory entp',
    'author': 'maulik',
    'license': 'LGPL-3',
    'description': """inventory entp""",
    'website': 'https://www.odoo.com',

    "depends": [
        'base','sale'
    ],
    "data": [
         # "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/stock_picking_view.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
