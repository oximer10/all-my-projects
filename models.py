from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()