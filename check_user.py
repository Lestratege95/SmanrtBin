import os
import sys
import django

# Ajouter le répertoire backend au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    user = User.objects.get(username='Taff')
    print(f"User found: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Is staff: {user.is_staff}")
except User.DoesNotExist:
    print("User 'Taff' does not exist")
except Exception as e:
    print(f"Error: {str(e)}") 