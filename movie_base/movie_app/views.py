from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse	
from django.db.models import Q

from .models import Movie, Review, Category, Actor, Genre
from .forms import ReviewForm, RatingForm, MyForm


def user_form(request):
	form = MyForm()
	return render(request, 'movie_app/form_template.html', {'form':form})

class FilterMoviesView(ListView):
	'''Список фильмов по фильтру'''
	def get_queryset(self):
		queryset = Movie.objects.filter(
			Q(year__in=self.request.GET.getlist('year')) | 
			Q(genres__in=self.request.GET.getlist('genre'))).distinct()
		return queryset

class GenreYear:
	'''Жанры и годы выпуска фильмов'''
	def get_genres(self):
		return Genre.objects.all()

	def get_years(self):
		return Movie.objects.filter(draft=False).values('year').distinct()

class MoviesView(GenreYear, ListView):
	'''Список фильмов'''
	model = Movie
	queryset = Movie.objects.filter(draft=False)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['categories'] = Category.objects.all()
		return context

	# context_object_name = 'movies'
	# template_name = 'movie_app/movies.html'
	
class MovieDetailView(GenreYear, DetailView):
	'''Страница с подробным описанием конкретного фильма'''
	model = Movie
	slug_field = 'url'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['star_form'] = RatingForm()
		return context
	
class ActorView(GenreYear, DetailView):
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

class AddStarRating(View):
	'''Добавление рейтинга фильму'''
	def get_client_ip(self):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip
		
	def post(self, request):
		form = RatingForm(request.POST)
		if form.is_valid():
			Rating.objects.update_or_create(
				ip=self.get_client_ip(request),
				movie_id=int(request.POST.get("movie")),
				defaults={'star_id':int(request.POST.get('star'))}
				)
			return HttpResponse(status=201)
		else:
			return HttpResponse(status=400)

class Search(ListView):
	'''Реализацуия поиска по названию'''
	def get_queryset(self):
		return Movie.objects.filter(title__icontains=self.request.GET.get('search'))

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['search'] = self.request.GET.get('search')
		return context