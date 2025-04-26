from django.contrib import admin, messages
from django import forms
from .models import PromptRequest, PromptResponse
from summarizer.database_model.request_response import RequestResponse

class PromptRequestForm(forms.ModelForm):

    class Meta:
        model = PromptRequest
        fields = ('file', 'prompt', 'created_by')

    def __init__(self, *args, **kwargs):
        super(PromptRequestForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False


class PromptRequestAdmin(admin.ModelAdmin):

    def get_changeform_initial_data(self, request):
        get_data = super(PromptRequestAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data  
    

    exclude = ['processed_internally', 'processed_externally']
    list_display = ['title', 'processed_internally',  'processed_externally', 'accepted', 'created_by', 'created']
    list_filter = ['title', 'processed_internally',  'processed_externally', 'accepted', 'created_by', 'created']


    actions = ['validate_internally', 'summarize_internally', 'summarize_externally']

    @admin.action(description='Validate request with local model')
    def validate_internally(self, request, queryset):
        if len(queryset) > 1:
            return messages.error(request, 'Please select only one prompt at a time for processing, to save resources')
        RequestResponse.validate_internally(self, queryset)
    
    @admin.action(description='Summarize text with local model')
    def summarize_internally(self, request, queryset):
        if len(queryset) > 1:
            return messages.error(request, 'Please select only one prompt at a time for processing, to save resources')
        RequestResponse.summarize_internally(self, queryset)

    @admin.action(description='Summarize text with external model')
    def summarize_externally(self, request, queryset):
        RequestResponse.summarize_externally(self, queryset)
                

class PromptResponseAdmin(admin.ModelAdmin):

    readonly_fields=('prompt_request', 'response', 'internal', 'external')

    list_display = ['get_prompt_name', 'internal', 'external', 'created']
    list_filter = ['prompt_request', 'internal', 'external', 'created']

    def get_prompt_name(self, obj):
        return obj.prompt_request.title

admin.site.register(PromptRequest, PromptRequestAdmin)
admin.site.register(PromptResponse, PromptResponseAdmin)