from django.urls import path
from summarizer.views import homeView

urlpatterns = [
    path('', homeView.HomeView.home, name='index'),
]