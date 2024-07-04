from django.db import models


class Platform(models.Model):
    name: models.CharField = models.CharField(max_length=100)


class Publisher(models.Model):
    name = models.CharField(max_length=100)


class Developer(models.Model):
    name = models.CharField(max_length=100)


class Game(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()

    platform = models.ForeignKey(
        Platform, on_delete=models.CASCADE, related_name='games'
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name='games'
    )
    developer = models.ForeignKey(
        Developer, on_delete=models.CASCADE, related_name='games'
    )

    def __str__(self):
        return f'{self.title} ({self.release_date})'
