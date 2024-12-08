{
    'name' : 'Estate Send Mail',
    'version' : '1.0',
    'summary': 'Estates Send Email',
    'description': "Estates Send Email",
    'license': 'LGPL-3',
    'category': 'Training/Estate',
    'depends' : ['estate','mail','contacts'],
    'data': [
        "data/mail_server_data_config.xml",
        "data/estate_property_email_template_data.xml",
        "views/estate_property_views.xml",
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
