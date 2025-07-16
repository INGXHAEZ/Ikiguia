import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikiguia.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
password = "admin123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superusuario creado exitosamente")
else:
    print("⚠️ El superusuario ya existe")
