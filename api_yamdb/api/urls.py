from api.views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                       ReviewsViewSet, TitlesViewSet)
from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
]
