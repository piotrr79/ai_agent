from django.contrib import admin
from .models import PromptCategory, PromptRequest, PromptResponse, Template
    
#class PromptCategory(admin.ModelAdmin):
#    pass

#class PromptRequest(admin.ModelAdmin):
#    pass

#class PromptResponse(admin.ModelAdmin):
#    pass

#class Template(admin.ModelAdmin):
#    pass

admin.site.register(PromptCategory)
admin.site.register(PromptRequest)
admin.site.register(PromptResponse)
admin.site.register(Template)