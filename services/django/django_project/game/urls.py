from django.urls import path

import game.views as game_views

# Create your views here.
urlpatterns = [
    path('', game_views.front_page, name='front_page'),
    path('import-games/', game_views.get_games_from_api, name='import_games'),
    path('post-games/', game_views.post_games, name='post_games'),
]
