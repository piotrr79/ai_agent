from django.db import models
from django.contrib.auth.models import User

class PromptCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_reference = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prompt_category'

class PromptInternalRequest(models.Model):    

    def user_directory_path(self, instance, filename): 
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
        return 'user_{0}/{1}'.format(instance.user.id, filename) 
    
    category = models.ForeignKey('PromptCategory', on_delete=models.CASCADE)
    prompt = models.TextField()
    file = models.FileField(upload_to = user_directory_path, blank=True, null=True) 
    accepted_internally = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_internal_request'

class PromptExternalRequest(models.Model):    
    
    category = models.ForeignKey('PromptCategory', on_delete=models.CASCADE)
    prompt = models.TextField()
    accepted_internally = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_external_request'

    def save_model(self, request, instance, form, change):
        user = request.user 
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.save()
        form.save_m2m()
        return instance

class PromptInternalResponse(models.Model):
    prompt_request = models.ForeignKey('PromptInternalRequest', on_delete=models.CASCADE)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_internal_response'

class PromptExternalResponse(models.Model):
    prompt_request = models.ForeignKey('PromptExternalRequest', on_delete=models.CASCADE)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_external_response'