# Generated by Django 3.2.13 on 2022-10-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblist', '0002_youtubelink'),
    ]

    operations = [
        migrations.AddField(
            model_name='weblink',
            name='title',
            field=models.CharField(default='none', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youtubelink',
            name='title',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
