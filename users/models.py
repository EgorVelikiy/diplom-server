from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

import os
import shutil

class User(AbstractUser):
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

@receiver(pre_delete, sender=User)
def auto_delete_user_storage(sender, instance, **kwargs):
    if instance.username:
        path_to_files = os.path.join(settings.MEDIA_ROOT, instance.username)
        if os.path.isdir(path_to_files):
            shutil.rmtree(path_to_files)