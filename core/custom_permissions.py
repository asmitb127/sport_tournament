from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from core.models import CustomUser as User


class TokenAuthentications(TokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def __init__(self) -> None:
        self.keyword = 'Bearer'
        self.model = None
        return super().__init__()
