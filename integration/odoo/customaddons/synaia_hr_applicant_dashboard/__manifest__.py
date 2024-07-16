{
    'name': 'Dashboard HR Applicant - Call Center',
    'version': '17.0.1.0',
    'summary': 'Human Resources Dashboard',
    'sequence': 11,
    'depends': ['synaia_hr_applicant', 'base', 'web', 'board'],
    'data': [
        'views/sales_dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/web/static/lib/Chart/Chart.js',
            '/synaia_hr_applicant_dashboard/static/src/components/*.js',
            '/synaia_hr_applicant_dashboard/static/src/components/*.xml',
        ],
    },
    'icon': '/synaia_hr_applicant_dashboard/static/description/icon.png',
    'category': 'Human Resources',
    'author': 'Wilton Beltre - SYNAIA',
    'installable': True,
    'application': False,
    'auto_install': False,
}
