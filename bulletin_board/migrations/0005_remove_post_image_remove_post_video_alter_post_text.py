# Generated by Django 5.1 on 2024-10-08 16:26

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0004_remove_post_files_delete_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
    ]
