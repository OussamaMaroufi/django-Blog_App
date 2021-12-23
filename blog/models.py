from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.title  


    def get_absolute_url(self): # new
        return reverse('post-detail', args=[str(self.id)])  #return the full path as  a string  little bit defferrnt from redirect 