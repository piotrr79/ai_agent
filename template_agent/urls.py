from django.urls import path
from template_agent.views import homeView, generatorTest

urlpatterns = [
    path('', homeView.TemplateHomeView.home, name='index'),
    path('test', generatorTest.GeneratorTestView.generator_test, name='test'),
]