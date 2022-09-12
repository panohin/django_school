from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse	

from .models import Movie, Review
from .forms import ReviewForm

class MoviesView(ListView):
	'''Список фильмов'''
	model = Movie
	queryset = Movie.objects.filter(draft=False)
	# context_object_name = 'movies'
	# template_name = 'movie_app/movies.html'
	
class MovieDetailView(DetailView):
	'''Страница с подробным описанием конкретного фильма'''
	model = Movie
	slug_field = 'url'

	# def get(self, request, slug):
	# 	movie = get_object_or_404(Movie, url=slug)
	# 	return render(request, 'movie_app/movie_detail.html', {'movie':movie})

class UserTemplateView(TemplateView):
	template_name = 'movie_app/info.html'

class AddReview(View):
	'''Отзыв'''
	def post(self, request, pk):
		form = ReviewForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.movie_id = pk
			form.save()
		return redirect('movie_list_url')

def show_movie(reqiest):
	m = Movie.objects.all()
	return HttpResponse(m)
