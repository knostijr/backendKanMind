# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

# Lokale Importe
# (keine benötigt)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer für die Registrierung neuer Benutzer.

    Dieser Serializer verarbeitet die Validierung von Benutzernamen, E-Mails und 
    Passwörtern. Er stellt sicher, dass Passwörter den Django-Sicherheitsrichtlinien 
    entsprechen und korrekt bestätigt werden.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="Muss den Standard-Django-Passwortrichtlinien entsprechen."
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Muss exakt mit dem Passwort-Feld übereinstimmen."
    )

    class Meta:
        """
        Metadaten-Konfiguration für den RegistrationSerializer.
        """
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, attrs):
        """
        Feldübergreifende Validierung der Eingabedaten.

        Prüft insbesondere, ob 'password' und 'password_confirm' identisch sind.

        Args:
            attrs (dict): Die bereits einzeln validierten Feldwerte.

        Raises:
            serializers.ValidationError: Wenn die Passwörter nicht übereinstimmen.

        Returns:
            dict: Die validierten Daten.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """
        Erstellt einen neuen Benutzer-Datensatz in der Datenbank.

        Nutzt 'create_user' statt 'create', um sicherzustellen, dass das 
        Passwort korrekt gehasht gespeichert wird.

        Args:
            validated_data (dict): Die bereinigten und validierten Daten.

        Returns:
            User: Die neu erstellte Benutzer-Instanz.
        """
        # Entfernen der Bestätigung, da diese nicht im Model existiert
        validated_data.pop('password_confirm')
        
        # Erstellung über den Manager, um Hashing zu aktivieren
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer für die öffentliche Darstellung von Benutzerdaten.

    Wird verwendet, um Benutzerinformationen in API-Antworten zurückzugeben, 
    ohne sensible Daten wie Passwort-Hashes zu exponieren.
    """
    class Meta:
        """
        Metadaten-Konfiguration für den UserSerializer.
        """
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
