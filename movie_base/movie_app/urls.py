from django.contrib import admin
from django.urls import path

from .views import MoviesView, MovieDetailView, UserTemplateView, show_movie, AddReview, ActorView, FilterMoviesView


urlpatterns = [
    path('info', UserTemplateView.as_view()),
    path('filter', FilterMoviesView.as_view(), name='filter_url'),
    path('actor/<str:slug>', ActorView.as_view(), name='actor_detail_url'),
    path('', MoviesView.as_view(),  name='movie_list_url'),
    path('review/<int:pk>', AddReview.as_view(), name='add_review_url'),
    path('<slug:slug>', MovieDetailView.as_view(), name='movie_detail_url'),
]