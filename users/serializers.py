from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from file_share.models import File
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'password')
        read_only_fields = ['id']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        if 'is_staff' in validated_data:
            validated_data.pop('is_staff')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        print(self.context['request'])
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        if 'is_staff' in validated_data:
            print(user, instance)
            if not user.is_staff:
                validated_data.pop('is_staff')
        return super().update(instance, validated_data)
    
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['user', 'file_name', 'size']

class UserFilesSerializer(serializers.ModelSerializer):
    files = FilesSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'files')
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        print(user)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}