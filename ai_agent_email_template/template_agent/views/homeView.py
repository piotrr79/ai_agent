from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

class TemplateHomeView:
    """
    Home url welcome message
    """

    def __init__(self):
        pass

    def home(request):
        return HttpResponse("Welcome on AI Agent for email templates. Please go to /admin to log in")
