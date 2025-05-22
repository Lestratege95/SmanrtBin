from django.apps import AppConfig

class SmartBinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartbin'
    
    MODULES = {
        'smart_bins': {
            'name': 'Module Poubelles Intelligentes',
            'description': 'Gestion des poubelles connectées et leurs données',
            'icon': '🗑️',
            'permissions': ['view_smartbin', 'manage_smartbin']
        },
        'collection': {
            'name': 'Module Collecte des Déchets',
            'description': 'Suivi des ramassages et collectes',
            'icon': '🚚',
            'permissions': ['view_collection', 'manage_collection']
        },
        'tri_center': {
            'name': 'Module Centre de Tri',
            'description': 'Gestion des centres de tri et du traitement',
            'icon': '🏭',
            'permissions': ['view_tricenter', 'manage_tricenter']
        },
        'valorization': {
            'name': 'Module Valorisation & Recyclage',
            'description': 'Gestion des débouchés et stocks',
            'icon': '📦',
            'permissions': ['view_valorization', 'manage_valorization']
        },
        'users': {
            'name': 'Module Utilisateurs et Accès',
            'description': 'Gestion des profils et permissions',
            'icon': '👤',
            'permissions': ['view_users', 'manage_users']
        },
        'reporting': {
            'name': 'Module Reporting et Suivi',
            'description': 'Visualisation des performances',
            'icon': '📊',
            'permissions': ['view_reports', 'manage_reports']
        },
        'settings': {
            'name': 'Module Paramètres',
            'description': 'Configuration et intégrations',
            'icon': '⚙️',
            'permissions': ['view_settings', 'manage_settings']
        }
    } 