from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import uuid
import os

from users.models import User

def unique_user_file_path(instance, file_name):
    name, format = os.path.splitext(file_name)
    
    unique_file_name = f"{name}({uuid.uuid4().hex}){format}"

    file_path = f"{instance.user.username}/{unique_file_name}"

    return file_path


class File(models.Model):
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE,
                             verbose_name='User')
    file = models.FileField(upload_to=unique_user_file_path, default=None, verbose_name="file")
    file_name = models.CharField(max_length=255, default='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(blank=True, default=0)
    special_link = models.CharField(blank=True, default='', max_length=255)
    
    def save(self, *args, **kwargs):
        self.file_name = '_'.join(os.path.basename(self.file.name).split())
        self.size = self.file.size
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['user', 'uploaded_at']



@receiver(pre_delete, sender=File)
def auto_delete_file_from_storage(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)