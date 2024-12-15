from django.contrib import admin
from .models import Event, Category, Genre, Application
# Register your models here.

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Application)

