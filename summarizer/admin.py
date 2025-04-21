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
    
    readonly_fields=('internal', 'external')
    exclude = ['processed_internally', 'processed_externally']

    list_display = ['title', 'internal', 'external', 'processed_internally',  'processed_externally', 'accepted', 'created_by', 'created']
    list_filter = ['title', 'internal', 'external', 'processed_internally',  'processed_externally', 'accepted', 'created_by', 'created']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    actions = ['validate_with_slm', 'call_ai']

    @admin.action(description='Validate request with SLM internally')
    def validate_with_slm(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.processed_internally == False:
                prompt_object = PromptRequest.objects.get(pk=item)
                # ai_responsne = Connector.call_gpt(self, prompt_object.prompt)
                # prompt_response = ai_responsne
                prompt_response = 'Dummy response'
                prompt_response.save()
                prompt_object.processed_internally = True
                prompt_object.save()

    @admin.action(description='Send prompts to AI for selected request')
    def call_ai(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.accepted is True:
                if prompt_object.processed_externally == False:
                    prompt_object = PromptRequest.objects.get(pk=item)
                    ai_responsne = Connector.call_gpt(self, prompt_object.prompt)
                    prompt_response = ai_responsne
                    prompt_response.save()
                    prompt_object.processed_externally = True
                    prompt_object.save()
                

class PromptResponseAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response')

admin.site.register(PromptRequest, PromptRequestAdmin)
admin.site.register(PromptResponse, PromptResponseAdmin)