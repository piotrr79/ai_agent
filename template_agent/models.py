from django.db import models
from django.contrib.auth.models import User

class PromptCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_reference = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prompt_category'
                    
class PromptRequest(models.Model):    

    def user_directory_path(self, instance, filename): 
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
        return 'user_{0}/{1}'.format(instance.user.id, filename) 
    
    category = models.ForeignKey('PromptCategory', on_delete=models.CASCADE)
    prompt = models.TextField()
    file = models.FileField(upload_to = user_directory_path, blank=True, null=True) 
    title = models.CharField(max_length=255, blank=True, null=True) 
    name = models.CharField(max_length=255, blank=True, null=True) 
    surname = models.CharField(max_length=255, blank=True, null=True) 
    to = models.EmailField(max_length=255, blank=True, null=True) 
    cc = models.EmailField(max_length=255, blank=True, null=True) 
    signature = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_request'

    def save_model(self, request, instance, form, change):
        user = request.user 
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.save()
        form.save_m2m()
        return instance

class PromptResponse(models.Model):
    prompt_request = models.ForeignKey('PromptRequest', on_delete=models.CASCADE)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_response'

class Template(models.Model):
    
    def user_directory_path(self, instance, filename): 
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
        return 'user_{0}/{1}'.format(instance.user.id, filename) 
    
    prompt_request = models.ForeignKey('PromptRequest', on_delete=models.CASCADE)
    template = models.TextField()
    file = models.FileField(upload_to = user_directory_path, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'template'