from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'bio', 'website', 'profile_pic', 'role']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
            hash the password on update and then
            call the parent class's update method with validated data
        """
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
