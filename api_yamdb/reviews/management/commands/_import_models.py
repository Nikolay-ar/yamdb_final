import csv

from reviews.models import (Category, Comment, Genre, GenresTitles, Review,
                            Title)
from users.models import User


def import_categories():
    with open('static/data/category.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Category(id=row['id'],
                                name=row['name'],
                                slug=row['slug'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте category.csv произошла ошибка {error}')


def import_genres():
    with open('static/data/genre.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Genre(id=row['id'],
                             name=row['name'],
                             slug=row['slug'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте genre.csv произошла ошибка {error}')


def import_titles():
    with open('static/data/titles.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Title(id=row['id'],
                             name=row['name'],
                             year=row['year'],
                             category=Category.objects.get(
                                 id=row['category'])
                             )
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте titles.csv произошла ошибка {error}')


def import_genres_title():
    with open('static/data/genre_title.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = GenresTitles(id=row['id'],
                                    title=Title.objects.get(
                                        id=row['title_id']),
                                    genre=Genre.objects.get(
                                        id=row['genre_id']))
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте genre_title.csv произошла ошибка {error}')


def import_users():
    with open('static/data/users.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = User(id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте users.csv произошла ошибка {error}')


def import_review():
    with open('static/data/review.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Review(id=row['id'],
                              title=Title.objects.get(
                                  id=row['title_id']),
                              text=row['text'],
                              author=User.objects.get(
                                  id=row['author']),
                              score=row['score'],
                              pub_date=row['pub_date'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте review.csv произошла ошибка {error}')


def import_comments():
    with open('static/data/comments.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Comment(id=row['id'],
                               review=Review.objects.get(
                                   id=row['review_id']),
                               text=row['text'],
                               author=User.objects.get(
                                   id=row['author']),
                               pub_date=row['pub_date']
                               )
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте comments.csv произошла ошибка {error}')
