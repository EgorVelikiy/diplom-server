from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout')
] + router.urls