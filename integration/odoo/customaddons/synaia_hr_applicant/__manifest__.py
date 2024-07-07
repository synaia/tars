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
            '/web/static/lib/Chart/Chart.js',
            '/synaia_hr_applicant/static/src/js/custom_gauge.js',
            '/synaia_hr_applicant/static/src/xml/custom_gauge.xml',
            '/synaia_hr_applicant/static/src/js/custom_progress.js',
            '/synaia_hr_applicant/static/src/xml/custom_progress.xml',
            '/synaia_hr_applicant/static/src/js/custom_letter_chart.js',
            '/synaia_hr_applicant/static/src/xml/custom_letter_chart.xml',
        ],
    },
    'icon': '/synaia_hr_applicant/static/description/icon.png',
    'category': 'Human Resources',
    'author': 'Elmer Rodríguez, Wilton Beltre - SYNAIA',
    'installable': True,
    'application': False,
    'auto_install': False,
}
