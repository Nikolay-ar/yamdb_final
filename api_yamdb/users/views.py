from http import HTTPStatus

from api.permissions import IsAdmin
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import (GetTokenSerializer, SignUpSerializer,
                               UserSerializer)


@api_view(['POST'])
def signup_view(request):
    """Функция для получения кода авторизации на почту."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        new_user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
    except IntegrityError:
        error = settings.USERNAME_ERROR if User.objects.filter(
            username=username).exists() else settings.EMAIL_ERROR
        return Response(error, status=HTTPStatus.BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(new_user)
    send_mail(
        subject='Код подтверждения',
        message=f'Регистрация прошла успешно! '
                f'Код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
def confirmation_view(request):
    """Функция для получения токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, code):
        response = {'Неверный код'}
        return Response(response, status=HTTPStatus.BAD_REQUEST)
    token = str(RefreshToken.for_user(user).access_token)
    response = {'token': token}
    return Response(response, status=HTTPStatus.OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdmin, ]
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=['GET', 'PATCH'], url_path='me')
    def get_or_update_self(self, request):
        """Редактирование и получение информации профиля."""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data,
                            status=HTTPStatus.OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(user,
                                        data=request.data,
                                        partial=True, )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data,
                            status=HTTPStatus.OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTPStatus.BAD_REQUEST)
