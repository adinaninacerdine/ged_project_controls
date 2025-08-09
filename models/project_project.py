# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    # Champs de contrôle manuel
    x_manual_cliq_access = fields.Boolean(
        string='Accès Canal Cliq',
        help="Cocher pour autoriser l'accès au canal Cliq du département",
        default=False
    )
    
    x_manual_workdrive_access = fields.Boolean(
        string='Accès WorkDrive', 
        help="Cocher pour autoriser l'accès aux dossiers WorkDrive",
        default=False
    )
    
    x_authorized_users = fields.Text(
        string='Utilisateurs Autorisés',
        help="Liste des emails autorisés, séparés par des virgules\nExemple: user1@hurimoney.com,user2@hurimoney.com"
    )
    
    x_access_level = fields.Selection([
        ('read', 'Lecture'),
        ('write', 'Écriture'),
        ('admin', 'Administration')
    ], string='Niveau d\'Accès', help="Niveau de permissions à appliquer")
    
    # Champs informatifs (calculés)
    x_department = fields.Selection([
        ('INNOVATION', 'Innovation'),
        ('EXPANSION', 'Expansion'),
        ('RENTABILITÉ-PROCESS', 'Rentabilité & Process')
    ], string='Département GED', compute='_compute_department', store=True)
    
    x_cliq_channel = fields.Char(
        string='Canal Cliq',
        compute='_compute_ged_info',
        help="Canal Cliq du département"
    )
    
    x_workdrive_folder = fields.Char(
        string='Dossier WorkDrive',
        compute='_compute_ged_info', 
        help="Dossier WorkDrive du projet"
    )
    
    x_authorized_count = fields.Integer(
        string='Nb Utilisateurs',
        compute='_compute_authorized_count',
        help="Nombre d'utilisateurs autorisés"
    )
    
    @api.depends('name')
    def _compute_department(self):
        """Classification automatique du département basée sur le nom du projet"""
        for project in self:
            if not project.name:
                project.x_department = False
                continue
                
            name_lower = project.name.lower()
            
            if any(keyword in name_lower for keyword in ['technique', 'innovation', 'r&d', 'développement']):
                project.x_department = 'INNOVATION'
            elif any(keyword in name_lower for keyword in ['expansion', 'commercial', 'déploiement', 'marché']):
                project.x_department = 'EXPANSION'  
            elif any(keyword in name_lower for keyword in ['rentabilité', 'gouvernance', 'process', 'optimisation']):
                project.x_department = 'RENTABILITÉ-PROCESS'
            else:
                project.x_department = 'RENTABILITÉ-PROCESS'  # Par défaut
    
    @api.depends('x_department')
    def _compute_ged_info(self):
        """Calcul des informations GED selon le département"""
        department_mapping = {
            'INNOVATION': {
                'channel': 'innovation-projets',
                'folder_prefix': 'PROJETS_INNOVATION'
            },
            'EXPANSION': {
                'channel': 'expansion-projets',
                'folder_prefix': 'PROJETS_EXPANSION'
            },
            'RENTABILITÉ-PROCESS': {
                'channel': 'rentabilite-process',
                'folder_prefix': 'PROJETS_RENTABILITE_PROCESS'
            }
        }
        
        for project in self:
            mapping = department_mapping.get(project.x_department, {})
            project.x_cliq_channel = mapping.get('channel', '')
            
            if project.name and mapping.get('folder_prefix'):
                clean_name = ''.join(c for c in project.name if c.isalnum() or c in ' -_').replace(' ', '_')
                project.x_workdrive_folder = f"{mapping['folder_prefix']}/PRJ_{project.id}_{clean_name}"
            else:
                project.x_workdrive_folder = ''
    
    @api.depends('x_authorized_users')
    def _compute_authorized_count(self):
        """Compte le nombre d'utilisateurs autorisés"""
        for project in self:
            if project.x_authorized_users:
                emails = [email.strip() for email in project.x_authorized_users.split(',') if email.strip()]
                project.x_authorized_count = len(emails)
            else:
                project.x_authorized_count = 0
    
    def action_apply_permissions(self):
        """Action pour appliquer les permissions manuellement"""
        for project in self:
            if not project.x_authorized_users:
                continue
                
            try:
                # Log de l'action (en production, ici on appellerait les APIs)
                _logger.info(f"Application permissions projet {project.name}:")
                _logger.info(f"  - Cliq: {project.x_manual_cliq_access}")
                _logger.info(f"  - WorkDrive: {project.x_manual_workdrive_access}")
                _logger.info(f"  - Utilisateurs: {project.x_authorized_users}")
                _logger.info(f"  - Niveau: {project.x_access_level}")
                
                # Ici on appellerait les APIs Cliq et WorkDrive
                if project.x_manual_cliq_access:
                    self._apply_cliq_permissions(project)
                    
                if project.x_manual_workdrive_access:
                    self._apply_workdrive_permissions(project)
                    
                # Message utilisateur
                message = f"Permissions appliquées pour {project.name}"
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': message,
                        'type': 'success',
                        'sticky': False,
                    }
                }
                
            except Exception as e:
                _logger.error(f"Erreur application permissions {project.name}: {e}")
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': f"Erreur: {str(e)}",
                        'type': 'danger',
                        'sticky': True,
                    }
                }
    
    def _apply_cliq_permissions(self, project):
        """Applique les permissions Cliq (simulation pour l'instant)"""
        _logger.info(f"[SIMULATION] Ajout utilisateurs au canal #{project.x_cliq_channel}")
        # En production : appel API Cliq pour inviter les utilisateurs
        pass
    
    def _apply_workdrive_permissions(self, project):
        """Applique les permissions WorkDrive (simulation pour l'instant)"""  
        _logger.info(f"[SIMULATION] Ajout permissions {project.x_access_level} sur {project.x_workdrive_folder}")
        # En production : appel API WorkDrive pour ajouter permissions
        pass
    
    def action_revoke_permissions(self):
        """Action pour révoquer toutes les permissions"""
        for project in self:
            project.write({
                'x_manual_cliq_access': False,
                'x_manual_workdrive_access': False,
                'x_authorized_users': False,
                'x_access_level': False
            })
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Permissions révoquées',
                'type': 'info',
                'sticky': False,
            }
        }