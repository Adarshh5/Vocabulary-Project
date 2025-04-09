# Generated by Django 5.1.4 on 2025-04-09 11:41

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0010_alter_offlinecoaching_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
