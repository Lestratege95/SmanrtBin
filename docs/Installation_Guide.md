# Guide d'Installation et d'Utilisation de SmartBin

## Prérequis

### Système d'exploitation
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+ recommandé)

### Logiciels requis
- Docker et Docker Compose
- Git
- Un navigateur web moderne (Chrome, Firefox, Edge)

## Installation

### Option 1 : Installation avec Docker (Recommandé)

1. Cloner le repository :
```bash
git clone https://github.com/votre-username/smartbin.git
cd smartbin
```

2. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer le fichier .env avec vos configurations
```

3. Démarrer les services :
```bash
cd docker
docker-compose up -d
```

4. Accéder à l'application :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000/api
- Interface d'administration : http://localhost:8000/admin

### Option 2 : Installation manuelle

#### Backend

1. Créer un environnement virtuel :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer la base de données :
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Démarrer le serveur :
```bash
python manage.py runserver
```

#### Frontend

1. Installer les dépendances :
```bash
cd frontend
npm install
```

2. Démarrer l'application :
```bash
npm start
```

## Configuration initiale

1. Se connecter à l'interface d'administration :
   - URL : http://localhost:8000/admin
   - Utiliser les identifiants créés lors de l'installation

2. Créer les premiers types de poubelles :
   - Général
   - Recyclable
   - Organique
   - Dangereux

3. Ajouter les premières poubelles :
   - Nom
   - Emplacement
   - Type
   - Capacité

## Utilisation

### Tableau de bord
- Vue d'ensemble des statistiques
- État des poubelles en temps réel
- Alertes pour les poubelles pleines

### Gestion des poubelles
- Ajouter/modifier/supprimer des poubelles
- Mettre à jour le niveau de remplissage
- Marquer une poubelle comme collectée

### Historique des collectes
- Consulter l'historique des collectes
- Ajouter de nouvelles collectes
- Filtrer par date et poubelle

### Rapports
- Générer des rapports personnalisés
- Exporter les données
- Visualiser les tendances

## Maintenance

### Sauvegarde
```bash
# Sauvegarder la base de données
docker-compose exec db pg_dump -U smartbin smartbin > backup.sql

# Restaurer la base de données
docker-compose exec -T db psql -U smartbin smartbin < backup.sql
```

### Mise à jour
```bash
# Mettre à jour le code
git pull

# Reconstruire les conteneurs
docker-compose build
docker-compose up -d
```

## Dépannage

### Problèmes courants

1. **Le serveur ne démarre pas**
   - Vérifier les logs : `docker-compose logs`
   - S'assurer que les ports ne sont pas utilisés

2. **Erreurs de connexion à la base de données**
   - Vérifier les variables d'environnement
   - Redémarrer le conteneur de base de données

3. **Problèmes d'authentification**
   - Vérifier les tokens JWT
   - Réinitialiser le mot de passe administrateur

### Support

Pour toute assistance supplémentaire :
- Consulter la documentation complète
- Ouvrir une issue sur GitHub
- Contacter l'équipe de support 