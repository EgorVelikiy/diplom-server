import tzdata
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.generics import get_object_or_404
from file_share.permissions import IsOwnerOrReadOnly

from file_share.serializers import FileSerializer

from file_share.models import File
from users.models import User

class FilesViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['user',]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user']

    def get_permissions(self):
        if self.action in ['download', 'partial_update', 'destroy', 'retrieve']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ['list', 'create']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def list(self, request, user, *args, **kwargs):
        if request.user.is_staff and user:
            target_user = get_object_or_404(User, username=user)
            files = target_user.files
        else:
            files = request.user.files
        ser = self.serializer_class(files, many=True)
        return Response(ser.data)

    def destroy(self, request, pk=None,  *args, **kwargs):
        file = get_object_or_404(self.queryset, pk=pk)
        file.delete()
        return Response({'status': 'Ok'})
    
    def download(self, request, pk=None, *args, **kwargs):
        file = get_object_or_404(self.queryset, pk=pk)
        try:
            file.downloaded_at = timezone.now()
            file.save()
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
        print(file)
        return FileResponse(open(file.file.path, 'rb'), as_attachment=True)
    
    def partial_update(self, request, pk=None, *args, **kwargs):
        file = get_object_or_404(self.queryset, pk=pk)
        ser = self.serializer_class(file, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
    
    ## spesial_link