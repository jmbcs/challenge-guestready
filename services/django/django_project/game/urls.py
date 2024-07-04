from django.urls import path

import game.views as game_views

# Create your views here.
urlpatterns = [
    path('/', game_views.front_page, name='frontpage'),
]
