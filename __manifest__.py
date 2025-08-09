# -*- coding: utf-8 -*-
{
    'name': 'GED Project Controls',
    'version': '1.0.0',
    'category': 'Project',
    'summary': 'Contrôles manuels pour projets GED - Cliq et WorkDrive',
    'description': '''
GED Project Controls
====================
Module de contrôle manuel des accès projets :
* Autorisation Cliq par projet
* Autorisation WorkDrive par projet  
* Gestion utilisateurs autorisés
* Niveaux d'accès granulaires
* Sécurité maximale sans accès automatique
    ''',
    'author': 'HuriMoney',
    'website': 'https://hurimoney.com',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'data/access_levels_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}