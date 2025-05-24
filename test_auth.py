import requests
import json

# Première étape : obtenir le token
auth_url = "http://127.0.0.1:8000/api/token/"
auth_data = {
    "username": "koura",
    "password": "WorkHard"
}

try:
    # Obtenir le token
    auth_response = requests.post(auth_url, json=auth_data)
    print("Status Code (Auth):", auth_response.status_code)
    
    if auth_response.status_code == 200:
        tokens = auth_response.json()
        access_token = tokens['access']
        
        # Utiliser le token pour accéder à un endpoint protégé
        # Par exemple, la liste des utilisateurs
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # Test avec l'endpoint des utilisateurs
        users_url = "http://127.0.0.1:8000/api/users/"
        users_response = requests.get(users_url, headers=headers)
        
        print("\nTest de l'endpoint protégé :")
        print("Status Code:", users_response.status_code)
        print("Response Headers:", users_response.headers)
        print("Response Text:", users_response.text)
        
        if users_response.status_code == 200:
            print("Response JSON:", users_response.json())
    else:
        print("Erreur d'authentification:", auth_response.text)
        
except Exception as e:
    print("Error:", str(e)) 