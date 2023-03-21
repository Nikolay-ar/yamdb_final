from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_year


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(default=0)
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')


class PostTitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitlesSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context.get('view').kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'Нельзя добавлять больше одного отзыва')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comment
        read_only_fields = ('review',)
