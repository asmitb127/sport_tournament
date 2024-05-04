from rest_framework import permissions
from rest_framework import generics

from core.models import CustomUser as User
from core.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
