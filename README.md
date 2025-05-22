# SmartBin System

Système intelligent de gestion des déchets

## Description
SmartBin est une application web complète pour la gestion intelligente des déchets, comprenant :
- Un backend Django pour la gestion des données et l'API
- Un frontend React pour l'interface utilisateur
- Une base de données pour le stockage des informations

## Structure du Projet
```
/smart-bin-system/
├── /backend/          # Backend Django
├── /frontend-react/   # Frontend React
├── /data/             # Base de données
├── /docker/           # Configuration Docker
└── /docs/             # Documentation
```

## Prérequis
- Python 3.8+
- Node.js 14+
- Docker (optionnel)

## Installation
1. Cloner le repository
2. Installer les dépendances backend :
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Installer les dépendances frontend :
   ```bash
   cd frontend-react
   npm install
   ```

## Démarrage
1. Lancer le backend :
   ```bash
   cd backend
   python manage.py runserver
   ```
2. Lancer le frontend :
   ```bash
   cd frontend-react
   npm start
   ```

## Documentation
Consultez le dossier `/docs` pour la documentation détaillée de l'API et du système.

# DB_NAME=smartbin_db
# DB_USER=postgres
# DB_PASSWORD=postgres
# DB_HOST=localhost
# DB_PORT=5432