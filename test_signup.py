import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'projectSE.settings'
django.setup()

from django.test import Client
from django.urls import reverse
from client.models import User

client = Client()

# Test signup with all fields filled
post_data = {
    'name': 'Adam',
    'lastname': 'Snow',
    'email': 'adamSnow123@mail.tn',
    'password': 'testpass123'
}

print("Testing signup...")
response = client.post(reverse('add_user'), post_data)
print(f'Response Status: {response.status_code}')

# Check if user was created
user = User.objects.filter(email='adamSnow123@mail.tn').first()
if user:
    print(f'SUCCESS: User created!')
    print(f'  Email: {user.email}')
    print(f'  Name: {user.fullname}')
    print(f'  Role: {user.role}')
else:
    print('FAILED: User was not created')

# Show all users
print(f'\nTotal users in database: {User.objects.count()}')
