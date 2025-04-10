from django.contrib import admin
from django import forms
from .models import PromptRequest, PromptResponse
from summarizer.templates_generator.connector import Connector

class PromptRequestForm(forms.ModelForm):

    class Meta:
        model = PromptRequest
        exclude = ['processed']
        fields = ('file', 'prompt', 'created_by')

    def __init__(self, *args, **kwargs):
        super(PromptRequestForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False

class PromptRequestAdmin(admin.ModelAdmin):

    actions = ['call_ai']

    @admin.action(description='Send prompts to AI for selected request')
    def call_ai(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.processed == False:
                prompt_object = PromptRequest.objects.get(pk=item)
                ai_responsne = Connector.call_gpt(self, prompt_object.prompt)
                prompt_response = ai_responsne
                prompt_response.save()
                prompt_object.processed = True
                prompt_object.save()
                

class PromptResponse(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response')

admin.site.register(PromptRequest, PromptRequestAdmin)