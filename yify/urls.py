from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<int:pageNum>/', views.home, name='yts-home'),
    path('details/<int:id>/', views.details, name='yts-details'),
    path('search/', views.search_bar, name='search-bar'),
    path('search/<str:query>/', views.search, name='search'),
    path(
        'download/<str:t_hash>/<str:imdb>/<int:yify_id>/',
        views.download,
        name='download'
    ),
    path('queue/', views.queue, name='queue'),
    path('available/', views.available, name='available'),
    path(
        'available/details/<str:imdb>/', 
        views.available_details,
        name='available_details'
    ),
    path('watch/<str:imdb>/', views.watch, name='watch')
]
