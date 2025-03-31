from django.urls import path
from file_share.views import FilesViewSet


urlpatterns = [
    path('files/list/<user>', FilesViewSet.as_view({'get': 'list'})),
    path('files/<int:pk>', FilesViewSet.as_view({'delete': 'destroy'})),
    path('files/<int:pk>', FilesViewSet.as_view({'patch': 'partial_update'})),
    path('files/download/<int:pk>', FilesViewSet.as_view({'get': 'download'})),
    path('files/upload/', FilesViewSet.as_view({'post': 'create'})),
]
