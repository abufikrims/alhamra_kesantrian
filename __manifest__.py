# -*- coding: utf-8 -*-
{
    'name': "alhamra_kesantrian",

    'summary': """
        Modul Kesantrian IBS Alhamra
        """,

    'description': """
        Berisi modul pengelolaan kesantrian IBS Alhamra
    """,

    'author': "Cendana2000",
    'website': "http://www.cendana2000.com",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','alhamra_akademik'],

    # always loaded
    'data': [
         'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/kesantrian.xml',
        'views/hadits.xml',
        'views/nilai_tahfidz.xml',
        'views/quran.xml',
        'views/tahfidz_hadits.xml',
        'views/tahfidz_quran.xml',
        'views/tahsin.xml',
        'views/level_tahsin.xml',
        'views/mutabaah.xml',
        'views/orangtua_view.xml',
        'views/satpam_view.xml',
        'views/musyrif_view.xml',
        'views/menu.xml',
    ],
    'css': ['static/src/css/my_css.css'],
    'images': [],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}