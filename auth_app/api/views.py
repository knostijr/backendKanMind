# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Lokale Importe
from .serializers import UserRegistrationSerializer, UserSerializer


class RegistrationView(APIView):
    """
    API-Endpunkt für die Registrierung neuer Benutzer.
    
    Ermöglicht es Besuchern, ein neues Benutzerkonto zu erstellen, 
    indem sie die erforderlichen Daten übermitteln.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Verarbeitet die Registrierungsdaten und erstellt einen neuen User.

        Args:
            request: Das Request-Objekt, das die Benutzerdaten im Body enthält.

        Returns:
            Response: JSON mit Benutzerdaten bei Erfolg (201) 
                      oder Fehlermeldungen bei Validierungsfehlern (400).
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "User successfully registered"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    API-Endpunkt für die Authentifizierung von Benutzern.
    
    Prüft die Anmeldedaten und stellt bei Erfolg JSON Web Tokens (JWT) aus.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validiert die Anmeldedaten und generiert Access- sowie Refresh-Tokens.

        Args:
            request: Das Request-Objekt, das 'username' und 'password' enthält.

        Returns:
            Response: JSON mit Refresh-Token, Access-Token und Benutzerprofil bei Erfolg (200),
                      Fehlermeldung bei fehlenden Daten (400) oder falschen Credentials (401).
        """
        username = request.data.get('username')
        password = request.data.get('password')

        # Überprüfung auf Vollständigkeit der Daten
        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authentifizierung gegen die Django-Benutzerdatenbank
        user = authenticate(username=username, password=password)

        if user is not None:
            # Erstellung der JWT-Tokens für den authentifizierten User
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })

        # Rückgabe bei ungültigen Anmeldedaten
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )
