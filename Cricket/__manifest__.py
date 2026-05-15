{
    "name": "Cricket Tournament management",
    'version': '19.0.1.0.0',
    'category': 'Website',
    'summary': 'Cricket manage',
    'author': 'maulik',
    'license': 'LGPL-3',
    'description': """ Cricket """,
    'website': 'https://www.odoo.com',

    "depends": [
        'base', 'contacts','sale'
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "reports/team_point_report_view.xml",
        "views/player_view.xml",
        "views/team_view.xml",
        "views/matches_view.xml",
        "views/venue_view.xml",
        "views/team_name_view.xml",
        "views/tournament_view.xml",
        "views/coach_view.xml",
        "views/point_table_view.xml",
        "views/partner_view.xml",
        "views/user_view.xml",
        "wizard/match_runs_wizard_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
