# Generated by Django 4.1 on 2022-09-06 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer',
            field=models.URLField(blank=True, default='#', null=True, verbose_name='Ссылка на трейлер'),
        ),
    ]