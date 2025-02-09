from django.http import HttpResponse
from template_agent.templates_generator.email_generator import EmailGenerator

class GeneratorTestView:
    """
    Home url welcome message
    """

    def __init__(self):
        pass

    def __pass_self(self):
        return self

    def generator_test(request):
        responsne = EmailGenerator.generate_email_content(GeneratorTestView.__pass_self)
        return HttpResponse(responsne)
