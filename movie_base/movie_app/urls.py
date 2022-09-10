from django.contrib import admin
from django.urls import path

from .views import MoviesView, MovieDetailView, UserTemplateView


urlpatterns = [
    path('info', UserTemplateView.as_view()),

    path('<slug:slug>', MovieDetailView.as_view(), name='movie_detail_url'),
    path('', MoviesView.as_view(),  name='movie_list_url'),
    
]