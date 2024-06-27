{
    'name': 'Custom HR Applicant - Call Center',
    'version': '17.0.1.0',
    'summary': 'Human Resources',
    'sequence': 10,
    'depends': ['hr_recruitment'],
    # 'depends': ['hr_recruitment', 'web'],
    'data': [
        'views/all_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/synaia_hr_applicant/static/src/js/custom_gauge.js',
            '/synaia_hr_applicant/static/src/xml/custom_gauge.xml',
        ],
    },
    'icon': '/synaia_hr_applicant/static/description/icon.png',
    'category': 'Human Resources',
    'author': 'Elmer Rodríguez, Wilton Beltre - SYNAIA',
    'installable': True,
    'application': False,
    'auto_install': False,
}
