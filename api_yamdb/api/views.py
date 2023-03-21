from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdminOrReadOnly,
                             IsAuthorOrIsModeratorOrAdminOrReadOnly)
from api.serializers import (CategoriesSerializer, CommentSerializer,
                             GenresSerializer, PostTitlesSerializer,
                             ReviewSerializer, TitlesSerializer)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Genre, Review, Title


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return PostTitlesSerializer
        return TitlesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrIsModeratorOrAdminOrReadOnly,)

    def title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title())


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrIsModeratorOrAdminOrReadOnly,)

    def review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review())
