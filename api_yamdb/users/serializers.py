from django.conf import settings
from rest_framework import serializers
from users.models import User
from users.validators import username_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('username', 'email'),
                message=('Пользователь с таким email уже существует')
            )
        ]


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=settings.FIELD_EMAIL_LENGTH)
    username = serializers.CharField(max_length=settings.FIELD_MAX_LENGTH,
                                     validators=[username_validator])

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=settings.FIELD_TOKEN_LENGTH,
        validators=[username_validator]
    )
    confirmation_code = serializers.CharField(
        max_length=settings.FIELD_TOKEN_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
