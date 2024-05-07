from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import CustomUser as User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    full_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'nationality', 'full_name')

    def create(self, validated_data):
        full_name = validated_data['full_name'].split(' ')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=' '.join(full_name[:len(full_name)-1]),
            last_name=full_name[-1],
            phone_number=validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

