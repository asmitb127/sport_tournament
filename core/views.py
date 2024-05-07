from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.core import serializers
from django.contrib.auth import authenticate

from core.models import CustomUser as User
from core.serializers import RegisterSerializer
from core.custom_permissions import TokenAuthentications


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class Userlogin(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email, password=password)
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'credentials': ['Incorrect email or password credential.']}, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(views.APIView):
    authentication_classes = [TokenAuthentications]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        try:
            token = Token.objects.get(user= request.user)
            token.delete()
            return Response({'logout': ['User Logged out Succesfully.']}, status=status.HTTP_200_OK)

        except Token.DoesNotExist as e:
            return Response({'token': ['Invalid token provided.']}, status=status.HTTP_400_BAD_REQUEST)


