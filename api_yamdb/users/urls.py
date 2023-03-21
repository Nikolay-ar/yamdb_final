from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, confirmation_view, signup_view

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('signup/', signup_view),
    path('token/', confirmation_view),
]
