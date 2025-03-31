from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.db import models
from django.dispatch import receiver
from django.conf import settings

import os
import shutil

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

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