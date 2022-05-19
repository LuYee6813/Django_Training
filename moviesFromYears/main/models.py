from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.title} 上映於 {self.year}'