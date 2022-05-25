from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    about = models.TextField(null=True)
    location = models.CharField(max_length=255,null=True)

    def __str__(self):
        return f'{str(self.user)} - profile'

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    
    def __str__(self):
        return f'{self.author} - post'

