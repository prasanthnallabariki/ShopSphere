from rest_framework import serializers
from accounts.models import User
from accounts.services.auth_service import AuthService
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
    def create(self, validated_data):
        return AuthService.register_user(validated_data)

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = RefreshToken(attrs["refresh"])
        return attrs

    def save(self, **kwargs):
        self.token.blacklist()