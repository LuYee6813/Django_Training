from django.db import models
# 引入內建認證模組的獲取使用者函數
from django.contrib.auth.models import User

# post模組
import uuid 
from datetime import datetime


class Profile(models.Model):
    # 依附現有的使用者做選擇
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images', default='default_profileimage.jpeg')
    location = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images")
    author_img = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user