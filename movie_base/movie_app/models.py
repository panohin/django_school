from statistics import mode
from tabnanny import verbose
from django.db import models
from datetime import date
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    '''Категории'''
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Actor(models.Model):
    '''Актёры и режиссёры'''
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')
    
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Актёр или режиссер'
        verbose_name_plural = 'Актёры и режиссеры'

        
class Genre(models.Model):
    '''Жанры'''
    name = models.CharField('Название жанра', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Movie(models.Model):
    '''Фильмы'''
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=300)
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2019)
    country = models.CharField('Страна', max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актёр', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='указывать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США', default=0, help_text='указывать сумму в долларах'
        )
    fees_in_world = models.PositiveIntegerField(
        'Сборы в мире', default=0, help_text='указывать сумму в долларах'
        )
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True
        )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)
    trailer = models.URLField('Ссылка на трейлер', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.review_set.filter(parent__isnull=True       )

    def get_absolute_url(self):
        return reverse('movie_detail_url', kwargs={'slug':self.url})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieShot(models.Model):
    '''Кадры из фильма'''
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Кадры из фильма'
        verbose_name = 'Кадр из фильма'

class RatingStar(models.Model):
    '''Звезда рейтинга'''
    value = models.PositiveSmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'

class Rating(models.Model):
    '''Рейтинг'''
    ip = models.CharField('IP', max_length=15)
    star = models.ForeignKey(
        RatingStar, verbose_name='Количество звёзд', on_delete=models.CASCADE
        )
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Review(models.Model):
    '''Отзывы к фильму'''
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)
    text = models.TextField('Отзыв')
    email = models.EmailField()
    name = models.CharField('Имя автора отзыва', max_length=70)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, null=True, blank=True
        )

    def __str__(self):
        return f'{self.movie} - {self.name} - {self.text}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'