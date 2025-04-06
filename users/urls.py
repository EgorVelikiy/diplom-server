from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView
from knox import views

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', views.LogoutView.as_view(), name='logout')
] + router.urls