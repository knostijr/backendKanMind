"""
Zentrale URL-Konfiguration des core-Projekts.

Dieses Modul fungiert als Hauptverteiler (Root URLconf). Es delegiert die 
eingehenden Anfragen basierend auf ihren Pfaden an das Django-Admin-Interface 
oder die spezifischen API-Module der installierten Apps.

Struktur:
- /admin/         : Zugriff auf das Django Administration Backend.
- /api/           : Einstiegspunkt für alle Authentifizierungs-Ressourcen (auth_app).
- /api/           : Einstiegspunkt für alle Kanban-Ressourcen (kanban_app).
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Schnittstelle für das integrierte Django-Administrations-Backend.
    path('admin/', admin.site.urls),

    # Einbindung der Authentifizierungs-Endpunkte (Login, Registrierung).
    # Durch das Präfix 'api/' sind diese unter /api/login/ etc. erreichbar.
    path('api/', include('auth_app.api.urls')),

    # Einbindung der Kanban-Kernressourcen (Boards, Tasks, Kommentare).
    # Diese teilen sich das 'api/'-Präfix für eine konsistente URL-Struktur.
    path('api/', include('kanban_app.api.urls')),
]