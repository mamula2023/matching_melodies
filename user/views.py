from django.views.generic import TemplateView

import json
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin

class LoginView(TemplateView):
    template_name = 'login.html'

class SignUpView(TemplateView):
    template_name = 'signup.html'

