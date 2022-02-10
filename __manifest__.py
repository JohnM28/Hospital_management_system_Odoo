{
    'name': 'hms',
    'summary': 'Hospital Management System Module',
    'depends': ['base','crm'],
    'data': [
        'views/hms_views.xml',
        'views/department_views.xml',
        'views/doctor_view.xml',
        'views/log_view.xml',
        'views/crm_inherit_views.xml'
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/template.xml',

    ]
}