from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField()
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'bio', 'website', 'profile_pic', 'role', 'coins']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')  # Access the request object
        if request and request.user == instance:
            representation['email'] = instance.email
            representation['coins'] = instance.coins
        else:
            representation.pop('email', None) 
            representation.pop('coins', None)

        return representation


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

