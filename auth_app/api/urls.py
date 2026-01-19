# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.urls import path

# Lokale Importe
from .views import LoginView, RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]