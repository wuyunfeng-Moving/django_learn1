import datetime

from django.db import models
from django.utils import timezone


class WebLink(models.Model):
    web_address = models.URLField(max_length=200)
    language_scores = models.FloatField()
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.web_address

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class YoutubeLink(models.Model):
    address = models.CharField(max_length=200)
    score = models.FloatField()
    title = models.CharField(max_length=200)
    words_num = models.IntegerField()
    timelength = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return 'www.youtube.com/watch?v=' + self.address

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)