from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from .models import Movie

class MoviesView(View):
	'''Список фильмов'''
	def get(self, request):
		movies = Movie.objects.all()
		return render(request, 'movie_app/movies.html', {'movies':movies})

class MovieDetailView(View):
	'''Страница с подробным описанием конкретного фильма'''
	def get(self, request, slug):
		movie = get_object_or_404(Movie, url=slug)
		return render(request, 'movie_app/movie_detail.html', {'movie':movie})