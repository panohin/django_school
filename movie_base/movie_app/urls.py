from django.contrib import admin
from django.urls import path

from .views import MoviesView, MovieDetailView, UserTemplateView, show_movie, AddReview, ActorView


urlpatterns = [
    path('info', UserTemplateView.as_view()),
    path('<slug:slug>', MovieDetailView.as_view(), name='movie_detail_url'),
    path('actor/<int:pk>', ActorView.as_view(), 'actor_detail_url'),
    path('', MoviesView.as_view(),  name='movie_list_url'),
    path('review/<int:pk>', AddReview.as_view(), name='add_review_url'),
]