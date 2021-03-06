from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import *
from .forms import ReviewForm


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    model = Movie
    movie = Movie.objects.filter(draft=False)


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parents', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMovieView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist('year')) | Q(genres__in=self.request.GET.getlist('genre')))
        return queryset
