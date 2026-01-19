# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.urls import path

# Lokale Importe
from .views import LoginView, RegistrationView

"""
URL-Konfiguration für die Benutzerauthentifizierung.

Diese Routen definieren die Endpunkte für den Identitätsprozess der Anwendung.
Alle hier definierten Pfade werden typischerweise unter einem Präfix 
wie '/api/auth/' oder direkt unter '/api/' eingebunden.
"""

urlpatterns = [
    # Endpunkt für die Erstellung eines neuen Benutzerkontos.
    # Erwartet POST-Anfragen mit Benutzername, E-Mail und Passwort.
    path('registration/', RegistrationView.as_view(), name='registration'),
    
    # Endpunkt für den Login bestehender Benutzer.
    # Prüft Anmeldedaten und gibt bei Erfolg JWT-Access- und Refresh-Tokens zurück.
    path('login/', LoginView.as_view(), name='login'),
]