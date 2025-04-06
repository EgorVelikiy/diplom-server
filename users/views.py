from rest_framework.viewsets import ModelViewSet
from users.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import login
from knox.views import LoginView as KView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from users.models import User
from users.serializers import UserFilesSerializer, UserSerializer
from users.permissions import IsOwnerOrReadOnly

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    filterset_fields = ['files',]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['files']

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ['list', 'destroy']: 
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserFilesSerializer
        else:
            return UserSerializer

class LoginView(KView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return super(LoginView, self).post(request, format=None)