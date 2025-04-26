from summarizer.ai_model.connector import Connector
from summarizer.ai_model.validator import Validator
from summarizer.constants import VALIDATION_PROMPT, SUMMARIZE_PROMPT
from ..models import PromptRequest, PromptResponse


class RequestResponse():
    """ RequestResponse class """

    def __init__(self):
        pass

    def validate_internally(self, queryset: object) -> None:
        """ Validate with internal model

            Returns:
                None
        """
        selected = queryset.values_list('pk', flat=True)
        prompt_objects = PromptRequest.objects.filter(pk__in=selected)
        for item in prompt_objects:
            if item.processed_internally == False:
                 # @ToDo - move max_new_tokens and temperature to configuration (db or .env) 
                ai_responsne = Validator.call_internal_model(self, VALIDATION_PROMPT + ': ' + item.prompt, 60, 0.5)
                prompt_response = PromptResponse(prompt_request=item, response=ai_responsne)
                prompt_response.internal = True
                prompt_response.save()
                item.processed_internally = True
                item.save()


    def summarize_internally(self, queryset: object) -> None:
        """ Summarize with internal model

            Returns:
                None
        """
        selected = queryset.values_list('pk', flat=True)
        prompt_objects = PromptRequest.objects.filter(pk__in=selected)
        for item in prompt_objects:
            if item.processed_internally == True:
                 # @ToDo - move max_new_tokens and temperature to configuration (db or .env) 
                ai_responsne = Validator.call_internal_model(self, SUMMARIZE_PROMPT + ': ' + item.prompt, 250, 0.5)
                prompt_response = PromptResponse(prompt_request=item, response=ai_responsne)
                prompt_response.internal = True
                prompt_response.save()
                item.processed_internally = True
                item.save()


    def summarize_externally(self, queryset: object) -> None:
        """ Summarize with external model

            Returns:
                None
        """
        selected = queryset.values_list('pk', flat=True)
        prompt_objects = PromptRequest.objects.filter(pk__in=selected)
        for item in prompt_objects:
            if item.accepted is True:
                if item.processed_externally == False and item.processed_internally == True:
                    ai_responsne = Connector.call_gpt(self, SUMMARIZE_PROMPT + ': ' + item.prompt)
                    prompt_response = PromptResponse(prompt_request=item, response=ai_responsne)
                    prompt_response.external = True
                    prompt_response.save()
                    item.processed_externally = True
                    item.save()