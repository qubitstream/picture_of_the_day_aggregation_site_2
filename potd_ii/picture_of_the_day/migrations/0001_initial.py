# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-03-23 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import picture_of_the_day.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='POTD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='title of the picture')),
                ('source_type', models.CharField(choices=[('unspecified', 'Unspecified source'), ('wikipedia_en', 'Wikipedia (English)')], default='unspecified', max_length=36)),
                ('is_published', models.BooleanField(default=True, verbose_name='is published')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique_for_date='potd_at')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('retrieved_from_source_url_at', models.DateTimeField(verbose_name='datetime retrieved from source URL')),
                ('potd_at', models.DateField(verbose_name='date on which this picture was "picture of the day"')),
                ('description', models.TextField(verbose_name='description of the picture')),
                ('width', models.PositiveIntegerField(default=0, editable=False, verbose_name='width of image')),
                ('height', models.PositiveIntegerField(default=0, editable=False, verbose_name='height of image')),
                ('image', models.ImageField(height_field='height', upload_to=picture_of_the_day.models.image_upload_path, verbose_name='picture of the day image file', width_field='width')),
                ('raw_scraping_data_image', models.TextField(blank=True, editable=False, verbose_name='raw scraping data for image')),
            ],
            options={
                'verbose_name_plural': 'pictures of the day',
                'ordering': ['-potd_at'],
                'verbose_name': 'picture of the day',
            },
        ),
        migrations.AlterUniqueTogether(
            name='potd',
            unique_together=set([('potd_at', 'source_type')]),
        ),
    ]
