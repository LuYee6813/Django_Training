from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,models.CASCADE)
    about = models.TextField(max_length=200)
    def __str__(self):
        return f'{self.user}'

class Post(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)

    
    
     