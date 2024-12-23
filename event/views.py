from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'homepage.html'
    def get(self, request):
        return super().get(request)

class EventsView(TemplateView):
    template_name = 'events.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class EventView(TemplateView):
    template_name = 'event-detail.html'

class EventCreateView(TemplateView):
    template_name = 'create-event.html'
