from django.contrib import admin

from game.models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'genre',
        'description',
        'release_date',
        'platform_name',
        'publisher_name',
        'developer_name',
    ]

    def publisher_name(self, obj):
        return obj.publisher.name

    publisher_name.short_description = (
        'Publisher'  # this will set the column header in the admin
    )

    def platform_name(self, obj):
        return obj.platform.name

    platform_name.short_description = (
        'Platform'  # this will set the column header in the admin
    )

    def developer_name(self, obj):
        return obj.developer.name

    developer_name.short_description = (
        'Developer'  # this will set the column header in the admin
    )


admin.site.register(Game, GameAdmin)
