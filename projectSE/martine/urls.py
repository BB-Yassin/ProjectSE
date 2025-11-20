from django.urls import include, path
from . import views
from client import views as client_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse
from django.shortcuts import redirect


def packages_redirect(request):
    return redirect('feedback:new')   # feedback form

urlpatterns = [
    path('', views.home, name='home'),
    # Replace the old packages path with this redirect
    path('login_signup/', client_views.addUser, name='add_user'),
    path('reclamations/', include('reclamations.urls', namespace='reclamations')),
      # << ADD THIS LINE

]



