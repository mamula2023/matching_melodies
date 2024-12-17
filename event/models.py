from django.db import models
from user.models import CustomUser
# Create your models here.



class Event(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="events")
    title = models.TextField(max_length=30, null=False, blank=False)
    description = models.TextField(max_length=300, blank=False, null=False)
    city = models.CharField(max_length=20, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=False)
    img = models.ImageField(upload_to='event_images/', null=True, blank=True) 
    
    payment = models.IntegerField(null=True)
    additional_info = models.TextField(max_length=100, blank=True, null=True)


    categories = models.ManyToManyField(to='Category', blank=True, related_name='events')
    genres =     models.ManyToManyField(to='Genre', blank=True, related_name='events')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=20, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=20, unique=True, blank=False, null=False)

    def __str__(self):
        return self.title
