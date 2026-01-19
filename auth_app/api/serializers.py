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
    Serializer für User-Registrierung
    Validiert Passwort und erstellt neuen User
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, attrs):
        """
        Validiere, dass beide Passwörter übereinstimmen
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """
        Erstelle User mit gehashtem Passwort
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer für User-Darstellung (ohne Passwort)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
