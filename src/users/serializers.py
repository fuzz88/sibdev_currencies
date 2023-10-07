from typing import Any, Dict

from rest_framework import exceptions, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

MyAuthenticationFailed = exceptions.AuthenticationFailed()
MyAuthenticationFailed.status_code = status.HTTP_400_BAD_REQUEST


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        try:
            return super().validate(attrs)
        except exceptions.AuthenticationFailed:
            raise MyAuthenticationFailed
