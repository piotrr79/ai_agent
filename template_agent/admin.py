from django.contrib import admin
from django import forms
from .models import PromptCategory, PromptRequest, PromptResponse, Template
from template_agent.templates_generator.email_generator import EmailGenerator
import inspect

class PromptRequestForm(forms.ModelForm):

    class Meta:
        model = PromptRequest
        exclude = ['processed']
        fields = ('category', 'prompt' , 'file', 'created_by')

    def __init__(self, *args, **kwargs):
        super(PromptRequestForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False

class PromptResponseForm(forms.ModelForm):

    class Meta:
        model = PromptResponse
        fields = ('prompt_request', 'response')

    def __init__(self, *args, **kwargs):
        super(PromptResponseForm, self).__init__(*args, **kwargs)
        self.fields['prompt_request'].widget.attrs['readonly'] = True
        self.fields['response'].widget.attrs['readonly'] = True

#class PromptCategory(admin.ModelAdmin):
#    pass

class PromptRequestAdmin(admin.ModelAdmin):

    actions = ['call_ai']

    @admin.action(description='Generate templates for selected request')
    def call_ai(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        # @ToDo - get selected records obj ids and prompts, and pass them to AI and model save
        for pk in selected:
            prompt_request_id = request.resolver_match.kwargs['prompt_request']
            ai_responsne = EmailGenerator.generate_email_content(self)
            prompt_response = PromptResponse(prompt_request=prompt_request_id, response= ai_responsne)
            prompt_response.save()

class PromptResponseAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response')

#class Template(admin.ModelAdmin):
#    pass

admin.site.register(PromptCategory)
admin.site.register(PromptRequest, PromptRequestAdmin)
admin.site.register(PromptResponse, PromptResponseAdmin)
admin.site.register(Template)