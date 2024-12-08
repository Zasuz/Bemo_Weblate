{
    'name': 'Customize Branding',
    'version': '1.0',
    'summary': 'Customize Branding',
    'description': 'Customize Branding',
    'license': 'LGPL-3',
    'category': 'Training/Estate',
    'depends': ['base', 'website','website_form'],
    'data': [
        'views/assets.xml',
        'views/snippets/feedback_form.xml',
        'views/website_user_feedback.xml',
        'views/home_page_template.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/data_default_navbar.xml',
        'views/menu.xml'
    ],
    'qweb': [
        # 'static/src/xml/menu.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
