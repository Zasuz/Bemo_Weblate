{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Estates, Properties, Houses',
    'description': "Estates, Properties, Houses",
    'license': 'LGPL-3',
    'category': 'Training/Estate',
    'depends': ['base', 'mail', 'report_xlsx'],
    'data': [
        'data/demo.xml',
        'data/change_demo_record.xml',

        'wizard/buyer_offer_wizard_views.xml',

        'reports/estate_property_buyer_views.xml',

        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/assets.xml',
        'views/widget_model_views.xml',
        'views/estate_property_template.xml',
        'views/estate_property_detail_template.xml',

        'views/res_user_views.xml',

        "security/res_groups.xml",
        "security/ir.model.access.csv",

        'views/estate_menu.xml',
    ],
    # 'demo': [
    #     'data/demo.xml',
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
