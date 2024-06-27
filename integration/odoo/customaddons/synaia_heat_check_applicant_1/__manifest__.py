{
    'name': 'HR Applicant - Lead Temperature',
    'version': '17.0.1.0',
    'summary': 'Human Resources',
    'sequence': 10,
    'depends': ['hr_recruitment'],
    'data': [
        'views/hr_applicant_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/synaia_heat_check_applicant_1/static/src/js/custom_gauge.js',
            '/synaia_heat_check_applicant_1/static/src/xml/custom_gauge.xml',
        ],
    },
    'category': 'Human Resources',
    'author': 'Elmer Rodríguez - SYNAIA',
    'installable': True,
    'application': False,
    'auto_install': False,
}
