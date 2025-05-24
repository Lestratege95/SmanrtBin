import os
import sys
import django

# Ajouter le répertoire backend au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\nListe des superusers :")
print("-" * 50)
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    for user in superusers:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is active: {user.is_active}")
        print(f"Is staff: {user.is_staff}")
        print("-" * 50)
else:
    print("Aucun superuser trouvé dans la base de données.") 