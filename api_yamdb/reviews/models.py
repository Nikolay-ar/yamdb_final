from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from reviews.validators import validate_year
from users.models import User


class NameSlugModel(models.Model):
    name = models.TextField(max_length=settings.FIELD_TEXT_LENGTH,
                            verbose_name='Имя')
    slug = models.SlugField(max_length=settings.FIELD_SLUG_LENGTH,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Category(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'Катагория (Тип)'
        verbose_name_plural = 'Категории (Типы)'


class Genre(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(max_length=settings.FIELD_TEXT_LENGTH,
                            verbose_name='Название произведения')
    year = models.PositiveSmallIntegerField(
        'Год выпуска', blank=True, null=True, db_index=True,
        validators=[validate_year],
    )
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre, through='GenresTitles',
                                   verbose_name='Жанр', )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)


class GenresTitles(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение:Жанры'
        verbose_name_plural = 'Произведения:Жанры'

    def __str__(self):
        return f'{self.title} {self.genre}'


class ReviewComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.author}'

    class Meta:
        abstract = True
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ['pub_date', 'review']


class Review(ReviewComment):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, "Значение не больше %(limit_value)."),
            MinValueValidator(1, "Значение не меньше %(limit_value).")],
        verbose_name='Оценка')

    class Meta(ReviewComment.Meta):
        verbose_name = 'Отзыв на произведение'
        verbose_name_plural = 'Отзывы на произведение'
        ordering = ['pub_date', 'title']
        constraints = [UniqueConstraint(fields=['author', 'title'],
                                        name='double_review')]
        default_related_name = 'reviews'


class Comment(ReviewComment):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               verbose_name='Произведение')

    class Meta(ReviewComment.Meta):
        default_related_name = 'comments'
