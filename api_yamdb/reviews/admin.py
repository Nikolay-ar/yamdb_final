from django.contrib import admin

from .models import Category, Comment, Genre, GenresTitles, Review, Title


class GenresTitlesAdmin(admin.TabularInline):
    model = GenresTitles


class TitleAdmin(admin.ModelAdmin):
    def genre_list(self, obj):
        return list(genre for genre in obj.genre.all())

    list_display = (
        'pk', 'name', 'year', 'genre_list', 'description', 'category')
    list_editable = ('category',)
    search_fields = ('year', 'name',)
    list_filter = ('name',)
    inlines = [GenresTitlesAdmin, ]
    genre_list.short_description = 'Жанр'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('score',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
