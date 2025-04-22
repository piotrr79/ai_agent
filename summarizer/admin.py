from django.contrib import admin
from django import forms
from .models import PromptRequest, PromptResponse
from summarizer.ai_model.connector import Connector
from summarizer.ai_model.validator import Validator

class PromptRequestForm(forms.ModelForm):

    class Meta:
        model = PromptRequest
        fields = ('file', 'prompt', 'created_by')

    def __init__(self, *args, **kwargs):
        super(PromptRequestForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False


class PromptRequestAdmin(admin.ModelAdmin):
    
    exclude = ['processed_internally', 'processed_externally']

    list_display = ['title', 'processed_internally',  'processed_externally', 'accepted', 'created_by', 'created']
    list_filter = ['title', 'processed_internally',  'processed_externally', 'accepted', 'created_by', 'created']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        # @ToDo - handle form validation error nicely
        if obj.processed_internally is False and obj.accepted is True:
            raise forms.ValidationError('Before accepting prompt must be processed internally with SLM')
        else:
            super().save_model(request, obj, form, change)

    actions = ['validate_with_slm', 'summarize_with_slm', 'summarize_with_llm']

    @admin.action(description='Validate request with SLM internally')
    def validate_with_slm(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        prompt = 'Does the text attached contains sensitive data? Answer Yes or NO.'
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.processed_internally == True:
                prompt_object = PromptRequest.objects.get(pk=item)
                ai_responsne = Validator.call_llama(self, prompt + prompt_object.prompt)
                prompt_response = PromptResponse(prompt_request=prompt_object, response=ai_responsne)
                prompt_response.internal = True
                prompt_response.save()
                prompt_object.processed_internally = True
                prompt_object.save()
    
    @admin.action(description='Summarize text with SLM internally')
    def summarize_with_slm(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        prompt = 'Summarize attached text:'
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.processed_internally == True:
                prompt_object = PromptRequest.objects.get(pk=item)
                ai_responsne = Validator.call_llama(self, prompt + prompt_object.prompt)
                prompt_response = PromptResponse(prompt_request=prompt_object, response=ai_responsne)
                prompt_response.internal = True
                prompt_response.save()
                prompt_object.processed_internally = True
                prompt_object.save()

    @admin.action(description='Summarize text with LLM externally')
    def summarize_with_llm(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        prompt = 'Summarize attached text:'
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.accepted is True:
                if prompt_object.processed_externally == False and prompt_object.processed_internally == True:
                    prompt_object = PromptRequest.objects.get(pk=item)
                    ai_responsne = Connector.call_gpt(self, prompt + prompt_object.prompt)
                    prompt_response = PromptResponse(prompt_request=prompt_object, response=ai_responsne)
                    prompt_response.external = True
                    prompt_response.save()
                    prompt_object.processed_externally = True
                    prompt_object.save()
                

class PromptResponseAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response', 'internal', 'external')

    list_display = ['prompt_request', 'internal', 'external', 'created']
    list_filter = ['prompt_request', 'internal', 'external', 'created']

admin.site.register(PromptRequest, PromptRequestAdmin)
admin.site.register(PromptResponse, PromptResponseAdmin)