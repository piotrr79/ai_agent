from django.urls import path
from template_agent.views import homeView

urlpatterns = [
    path('', homeView.TemplateHomeView.home, name='index'),
]