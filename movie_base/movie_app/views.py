from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse	

from .models import Movie

class MoviesView(ListView):
	'''Список фильмов'''
	model = Movie
	# object_list = Movie.objects.all()
	# print(queryset)
	template_name = 'movie_app/movies.html'
	
class MovieDetailView(View):
	'''Страница с подробным описанием конкретного фильма'''
	def get(self, request, slug):
		movie = get_object_or_404(Movie, url=slug)
		return render(request, 'movie_app/movie_detail.html', {'movie':movie})

class UserTemplateView(TemplateView):
	template_name = 'movie_app/info.html'

def show_movie(reqiest):
	m = Movie.objects.all()
	return HttpResponse(m)