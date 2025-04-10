from django.contrib import admin
from django import forms
from .models import PromptCategory, PromptInternalRequest, PromptInternalResponse, PromptExternalRequest, PromptExternalResponse
from summarizer.templates_generator.connector import Connector

class PromptInternalRequestForm(forms.ModelForm):

    class Meta:
        model = PromptInternalRequest
        exclude = ['processed']
        fields = ('category', 'file', 'prompt', 'created_by')

    def __init__(self, *args, **kwargs):
        super(PromptInternalRequestForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False

class PromptInternalResponseForm(forms.ModelForm):

    class Meta:
        model = PromptInternalResponse
        fields = ('prompt_request', 'response')

    def __init__(self, *args, **kwargs):
        super(PromptInternalResponseForm, self).__init__(*args, **kwargs)
        self.fields['prompt_request'].widget.attrs['readonly'] = True
        self.fields['response'].widget.attrs['readonly'] = True


class PromptExternalRequestForm(forms.ModelForm):

    class Meta:
        model = PromptExternalRequest
        exclude = ['processed']
        fields = ('category', 'prompt', 'created_by')


class PromptExternalResponseForm(forms.ModelForm):

    class Meta:
        model = PromptExternalResponse
        fields = ('prompt_request', 'response')

    def __init__(self, *args, **kwargs):
        super(PromptExternalResponseForm, self).__init__(*args, **kwargs)
        self.fields['prompt_request'].widget.attrs['readonly'] = True
        self.fields['response'].widget.attrs['readonly'] = True

class PromptInternalRequestAdmin(admin.ModelAdmin):

    actions = ['call_ai']

    @admin.action(description='Send prompts to AI for selected request')
    def call_ai(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptInternalRequest.objects.get(pk=item)
            if prompt_object.processed == False:
                prompt_object = PromptInternalRequest.objects.get(pk=item)
                ai_responsne = Connector.call_gpt(self, prompt_object.prompt)
                prompt_response = ai_responsne
                prompt_response.save()
                prompt_object.processed = True
                prompt_object.save()
                

class PromptExternalResponseAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response')

class PromptExternalRequestAdmin(admin.ModelAdmin):

    actions = ['call_ai']

    @admin.action(description='Send prompts to AI for selected request')
    def call_ai(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptExternalRequest.objects.get(pk=item)
            if prompt_object.processed == False:
                prompt_object = PromptExternalRequest.objects.get(pk=item)
                ai_responsne = Connector.call_gpt(self, prompt_object.prompt)
                prompt_response = ai_responsne
                prompt_response.save()
                prompt_object.processed = True
                prompt_object.save()
                

class PromptExternalResponseAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response')

admin.site.register(PromptCategory)
admin.site.register(PromptInternalRequest, PromptInternalRequestAdmin)
admin.site.register(PromptExternalResponse, PromptExternalResponseAdmin)