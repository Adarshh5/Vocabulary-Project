# Generated by Django 5.1.4 on 2025-01-17 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0005_usersessiondata'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='word',
            unique_together={('word_name', 'part_of_speech')},
        ),
    ]
