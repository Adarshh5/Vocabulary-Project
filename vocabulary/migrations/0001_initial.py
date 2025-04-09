# Generated by Django 5.1.4 on 2024-12-06 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_name', models.CharField(max_length=255)),
                ('definition', models.TextField()),
                ('part_of_speech', models.CharField(max_length=200)),
                ('example', models.TextField(blank=True, null=True)),
                ('hindi_meaning', models.CharField(blank=True, max_length=255, null=True)),
                ('Synonyms', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='productimg')),
            ],
        ),
    ]
