from django.db import models
from django.contrib.auth.models import User
from django import forms
class PromptRequest(models.Model):    

    def user_directory_path(self, instance, filename): 
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
        return 'user_{0}/{1}'.format(instance.user.id, filename) 
    
    title = models.CharField(max_length=255, default='')
    prompt = models.TextField()
    file = models.FileField(upload_to = user_directory_path, blank=True, null=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed_internally = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    processed_externally = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_request'

    is_cleaned = False
    
    def clean(self):
        if self.processed_internally is False and self.accepted is True:
            raise forms.ValidationError('Before accepting prompt must be processed internally')
        else:
            self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()

        super().save(*args, **kwargs)

class PromptResponse(models.Model):
    prompt_request = models.ForeignKey('PromptRequest', on_delete=models.CASCADE)
    response = models.TextField()
    internal = models.BooleanField(default=False)
    external = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        db_table = 'prompt_response'