from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from file_share.models import File
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'password')
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        validate_password(attrs['password'])
        if User.objects.filter(username=attrs['username']):
            raise ValidationError('The user with this username already exists')
        if User.objects.filter(email=attrs['email']):
            raise ValidationError('The user with this email already exists')
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        if 'is_staff' in validated_data:
            validated_data.pop('is_staff')
        return super().create(validated_data)
    
    def update(self, instance, validated_data): 
        user = self.context['request'].user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        if (not user.is_staff or user.id == instance.id):
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
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}