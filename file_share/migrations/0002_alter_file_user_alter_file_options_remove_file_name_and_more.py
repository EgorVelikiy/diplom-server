# Generated by Django 5.1.7 on 2025-03-29 22:29

import django.db.models.deletion
import file_share.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_share', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='users.user', verbose_name='User'),
        ),
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['user', 'uploaded_at'], 'verbose_name': 'File', 'verbose_name_plural': 'Files'},
        ),
        migrations.RemoveField(
            model_name='file',
            name='name',
        ),
        migrations.AddField(
            model_name='file',
            name='file_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='file',
            name='special_link',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(default=None, upload_to=file_share.models.unique_user_file_path, verbose_name='file'),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
