# Documentation de l'API SmartBin

## Base URL
```
http://localhost:8000/api/
```

## Authentification
L'API utilise JWT (JSON Web Tokens) pour l'authentification. Incluez le token dans l'en-tête de vos requêtes :
```
Authorization: Bearer <votre_token>
```

## Endpoints

### Poubelles (Bins)

#### Liste des poubelles
```
GET /bins/
```
Paramètres de requête optionnels :
- `status` : Filtrer par statut (empty, half, full, overflow)
- `type` : Filtrer par type (general, recyclable, organic, hazardous)
- `location` : Filtrer par emplacement

Réponse :
```json
[
  {
    "id": 1,
    "name": "Poubelle 1",
    "location": "Zone A",
    "type": "general",
    "status": "empty",
    "capacity": 100,
    "current_level": 0,
    "fill_percentage": 0,
    "last_collection": "2023-01-01T12:00:00Z",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "assigned_to": null
  }
]
```

#### Détails d'une poubelle
```
GET /bins/{id}/
```

#### Créer une poubelle
```
POST /bins/
```
Corps de la requête :
```json
{
  "name": "Nouvelle poubelle",
  "location": "Zone B",
  "type": "recyclable",
  "capacity": 100,
  "current_level": 0,
  "status": "empty"
}
```

#### Mettre à jour une poubelle
```
PUT /bins/{id}/
```
Corps de la requête : même format que la création

#### Supprimer une poubelle
```
DELETE /bins/{id}/
```

#### Mettre à jour le niveau d'une poubelle
```
POST /bins/{id}/update_level/
```
Corps de la requête :
```json
{
  "current_level": 50
}
```

#### Marquer une poubelle comme collectée
```
POST /bins/{id}/collect/
```

### Collectes (Collections)

#### Liste des collectes
```
GET /collections/
```
Paramètres de requête optionnels :
- `bin` : ID de la poubelle
- `date_after` : Date de début
- `date_before` : Date de fin

Réponse :
```json
[
  {
    "id": 1,
    "bin": 1,
    "bin_name": "Poubelle 1",
    "date": "2023-01-01T12:00:00Z",
    "notes": "Collecte effectuée"
  }
]
```

#### Détails d'une collecte
```
GET /collections/{id}/
```

#### Créer une collecte
```
POST /collections/
```
Corps de la requête :
```json
{
  "bin": 1,
  "date": "2023-01-01T12:00:00Z",
  "notes": "Collecte effectuée"
}
```

#### Supprimer une collecte
```
DELETE /collections/{id}/
```

## Codes de statut

- 200 : Succès
- 201 : Créé
- 400 : Requête invalide
- 401 : Non authentifié
- 403 : Accès refusé
- 404 : Non trouvé
- 500 : Erreur serveur

## Exemples d'utilisation

### JavaScript (avec Axios)
```javascript
const API_URL = 'http://localhost:8000/api';

// Récupérer toutes les poubelles
axios.get(`${API_URL}/bins/`)
  .then(response => console.log(response.data))
  .catch(error => console.error(error));

// Créer une nouvelle poubelle
axios.post(`${API_URL}/bins/`, {
  name: 'Nouvelle poubelle',
  location: 'Zone B',
  type: 'recyclable',
  capacity: 100,
  current_level: 0,
  status: 'empty'
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

### Python (avec requests)
```python
import requests

API_URL = 'http://localhost:8000/api'

# Récupérer toutes les poubelles
response = requests.get(f'{API_URL}/bins/')
print(response.json())

# Créer une nouvelle poubelle
data = {
    'name': 'Nouvelle poubelle',
    'location': 'Zone B',
    'type': 'recyclable',
    'capacity': 100,
    'current_level': 0,
    'status': 'empty'
}
response = requests.post(f'{API_URL}/bins/', json=data)
print(response.json())
``` 