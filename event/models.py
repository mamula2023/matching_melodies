from django.db import models
from user.models import CustomUser
from django.core.exceptions import ValidationError
# Create your models here.



class Event(models.Model):
    TYPE_CHOICES = [
            ('gig', 'Gig'),
            ('collaboration', 'Collaboration')
        ]
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="events")
    title = models.TextField(max_length=30, null=False, blank=False)
    description = models.TextField(max_length=300, blank=False, null=False)
    city = models.CharField(max_length=20, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateTimeField(null=True, blank=True)
    img = models.ImageField(upload_to='event_images/', null=True, blank=True, default='event_images/default-image.png') 
    
    payment = models.IntegerField(null=True, blank=True)
    additional_info = models.TextField(max_length=100, blank=True, null=True)

    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=False, blank=False, default='gig')
    categories = models.ManyToManyField(to='Category', blank=True, related_name='events')
    genres =     models.ManyToManyField(to='Genre', blank=True, related_name='events')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def clean(self):
        if self.event_type == 'gig' and self.date is None:
            raise ValidationError("date field is required for gig events")
        if self.event_type == 'collaboration' and self.date is not None:
            raise ValidationError("events of type collaboration does not have field date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=20, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=20, unique=True, blank=False, null=False)

    def __str__(self):
        return self.title
