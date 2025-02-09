from django.contrib import admin
from django import forms
from .models import PromptCategory, PromptRequest, PromptResponse, Template
from template_agent.templates_generator.connector import Connector
from template_agent.templates_generator.email_generator import EmailGenerator

class PromptRequestForm(forms.ModelForm):

    class Meta:
        model = PromptRequest
        exclude = ['processed']
        fields = ('category', 'prompt' , 'file', 'created_by', 'title', 'name', 'surname', 'to', 'cc', 'signature')

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


class TemplateForm(forms.ModelForm):

    class Meta:
        model = Template
        fields = ('prompt_request', 'template')

    #def __init__(self, *args, **kwargs):
    #    super(TemplateForm, self).__init__(*args, **kwargs)
    #    self.fields['prompt_request'].widget.attrs['readonly'] = True
    #    self.fields['template'].widget.attrs['readonly'] = True

#class PromptCategory(admin.ModelAdmin):
#    pass

class PromptRequestAdmin(admin.ModelAdmin):

    actions = ['call_ai']

    @admin.action(description='Generate templates for selected request')
    def call_ai(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # @ToDo - improve db performance by moving query out of the loop
        for item in selected:
            prompt_object = PromptRequest.objects.get(pk=item)
            if prompt_object.processed == False:
                prompt_object = PromptRequest.objects.get(pk=item)
                ai_responsne = Connector.call_gpt(self, prompt_object.prompt)
                email_template = EmailGenerator.generate_email_template(self, ai_responsne, prompt_object.title, prompt_object.name, prompt_object.surname, prompt_object.to, prompt_object.cc, prompt_object.signature)
                prompt_response = PromptResponse(prompt_request=prompt_object, response=EmailGenerator.stringify_ai_response(self, ai_responsne))
                prompt_response.save()
                template_object = Template(prompt_request=prompt_object, template=email_template)
                template_object.save()
                prompt_object.processed = True
                prompt_object.save()
                

class PromptResponseAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'response')

class TemplateAdmin(admin.ModelAdmin):
    readonly_fields=('prompt_request', 'template')

admin.site.register(PromptCategory)
admin.site.register(PromptRequest, PromptRequestAdmin)
admin.site.register(PromptResponse, PromptResponseAdmin)
admin.site.register(Template, TemplateAdmin)