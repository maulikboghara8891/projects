{
    "name": "crm demo",
    'version': '19.0.1.0.0',
    'category': 'Website',
    'summary': 'crm demo',
    'author': 'maulik',
    'license': 'LGPL-3',
    'description': """crm demo""",
    'website': 'https://www.odoo.com',

    "depends": [
        'base','sale','helpdesk',
        'helpdesk_fsm'
    ],
    "data": [
         "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "reports/timesheet_report.xml",
        "views/assignment_rule_view.xml",
        "views/auto_assignment_view.xml",
        "views/helpdesk_ticket_view.xml",
        "views/user_view.xml",
        "views/sale_order_view.xml",
        "views/project_task_view.xml",
        "views/account_analytic_line.xml"

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
