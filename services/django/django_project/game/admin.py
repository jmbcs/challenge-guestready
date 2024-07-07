from django.contrib import admin
from game.models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "genre",
        "release_date",
    ]


admin.site.register(Game, GameAdmin)
