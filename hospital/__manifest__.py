{
    "name": "Hospital ",
    'version': '19.0.1.0.0',
    "depends": [
        'base','sale','account','purchase',
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_confirm_wizard_view.xml",
        "reports/purchase_order_report_view.xml",
        "views/dr_view.xml",
        "views/sale_order.xml",
        "views/invoice.xml",
        "views/stock_picking_view.xml",
        "views/purchase_order_view.xml",
        "views/res_config_settings_view.xml",


    ],
    'assets':{
        'web.assets_backend':
            [
                "hospital/static/src/xml/list_button.xml"
            ],
              },
    'installable': True,
    'application': True,
}
