from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from core.models import CustomUser as User


class UserAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            return exceptions.AuthenticationFailed('Token not provided.')
        try:
            token = Token.objects.get(key=token.split('Bearer ')[-1])
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token!')
        request.user = token.user
        return True