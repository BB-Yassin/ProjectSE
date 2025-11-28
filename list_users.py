import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'projectSE.settings'
django.setup()
from client.models import User
users = User.objects.all()
print(f"Total users: {users.count()}")
for u in users:
    print(f"- {u.email} ({u.role})")
