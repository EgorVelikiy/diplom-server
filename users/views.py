from rest_framework.viewsets import ModelViewSet
from users.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import UserFilesSerializer, UserSerializer, LoginSerializer
from users.permissions import IsOwnerOrReadOnly

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['files',]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['files']

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserFilesSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ['list', 'destroy']: 
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [AllowAny()]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            login(request, user)
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key})
        
        return Response(serializer.errors, status=400)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response({"detail": "Successfully logged out."})
        except Token.DoesNotExist:
            return Response({"detail": "No token found for this user."})