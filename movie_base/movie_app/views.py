from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse	

from .models import Movie, Review, Category, Actor
from .forms import ReviewForm

class MoviesView(ListView):
	'''Список фильмов'''
	model = Movie
	queryset = Movie.objects.filter(draft=False)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['categories'] = Category.objects.all()
		return context

	# context_object_name = 'movies'
	# template_name = 'movie_app/movies.html'
	
class MovieDetailView(DetailView):
	'''Страница с подробным описанием конкретного фильма'''
	model = Movie
	slug_field = 'url'

	# def get(self, request, slug):
	# 	movie = get_object_or_404(Movie, url=slug)
	# 	return render(request, 'movie_app/movie_detail.html', {'movie':movie})

class ActorView(DetailView):
	'''Страница с подробным описанием актера или режиссера'''
	model = Actor
	slug_field = 'name'
	template_name = 'movie_app/actor.html'

class UserTemplateView(TemplateView):
	template_name = 'movie_app/info.html'

class AddReview(View):
	'''Отзыв'''
	def post(self, request, pk):
		movie = get_object_or_404(Movie, pk=pk)
		form = ReviewForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			if request.POST.get("parent", None):
				form.parent_id = int(request.POST.get("parent"))
			form.movie_id = pk
			form.save()
		return redirect(movie.get_absolute_url())

def show_movie(reqiest):
	m = Movie.objects.all()
	return HttpResponse(m)
