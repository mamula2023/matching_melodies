from django.db import models
from user.models import CustomUser
from event.models import Event, Genre
# Create your models here.

class Application(models.Model):
    possible_status = [
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('held', 'Held')
        ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event_applications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_applications')
    status = models.CharField(
            max_length=20,
            choices = possible_status,
            default='pending'
            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"Application by {self.user} for {self.event}"
 
