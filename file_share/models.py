from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
import os.path


def get_path(instance, file_name):
    unique_name, file_path = unique_file_path_and_name(instance.user, file_name)
    instance.file_name = unique_name
    instance.file_path = file_path
    return file_path


def unique_file_path_and_name(user, file_name):
    name, format = os.path.splitext(file_name)
    count = 1
    unique_name = file_name
    while user.files.filter(file_name=file_name).exists():
        unique_name = f"{name}({count}){format}"
        file_name = unique_name
        count += 1

    file_path = f"{user.username}/{unique_name}"
    return unique_name, file_path


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='files', on_delete=models.CASCADE,
                             verbose_name='user')
    file = models.FileField(upload_to=get_path, default=None, verbose_name="file")
    file_name = models.CharField(max_length=255, default='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloaded_at = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, default='')
    size = models.PositiveIntegerField(blank=True, default=0)
    special_link = models.CharField(blank=True, default='', max_length=255)
    
    def save(self, *args, **kwargs):
        if self.file_name:
            self_file_name = '_'.join(self.file_name.split())
            original_file_name = '_'.join(os.path.basename(self.file.name).split())
            if self_file_name != original_file_name:
                new_file_name, _ = os.path.splitext(self.file_name)
                _, original_file_extension = os.path.splitext(self.file.name)
                new_file_name = f'{new_file_name}{original_file_extension}'
                if self.id:
                    old_full_file_path = self.file.path
                    file_name, file_path = unique_file_path_and_name(self.user, new_file_name)
                    self.file_name = file_name
                    self.file.name = file_path
                    new_full_file_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
                    os.rename(old_full_file_path, new_full_file_path)
                else:
                    self.file.name = new_file_name

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