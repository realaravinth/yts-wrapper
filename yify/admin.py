from django.contrib import admin

from .models import Downloaded_movies, Downloading

admin.site.register(Downloading)
admin.site.register(Downloaded_movies)
