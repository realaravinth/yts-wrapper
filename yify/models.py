from datetime import datetime

from django.db import models

class Downloaded_movies(models.Model):
    download_by = models.CharField(max_length=100)
    downloaded_on = models.DateTimeField('downloaded on')
    title_long = models.CharField(max_length=200)
    year = models.IntegerField()
    yify_id = models.CharField(max_length=20)
    imdb_code = models.CharField(max_length=40, primary_key=True)
    genres = models.TextField()
    rating = models.IntegerField()
    description_intro = models.TextField()
    yt_trailer_code = models.CharField(max_length=40)
    size = models.CharField(max_length=20)
    runtime = models.IntegerField()
    def __str__(self):
        return self.title_long
    def was_downloaded_on(self):
        return self.downloaded_on >= timezone.now() - datetime.timedelta(days=1)
    class Meta:
        verbose_name_plural = "Yify Movies"

class Downloading(models.Model):
    download_by = models.CharField(max_length=100)
    downloaded_on = models.DateTimeField(default=datetime.now())
    title_long = models.CharField(max_length=200)
    year = models.IntegerField()
    yify_id = models.CharField(max_length=20)
    imdb_code = models.CharField(max_length=40, primary_key=True)
    genres = models.TextField()
    rating = models.IntegerField()
    description_intro = models.TextField()
    yt_trailer_code = models.CharField(max_length=40)
    size = models.CharField(max_length=20)
    runtime = models.IntegerField()
    
    progress = models.CharField(max_length=10)
    downloading = models.BooleanField()
    img_url = models.TextField()
    def __str__(self):
        return self.title_long
    def was_downloaded_on(self):
        return self.downloaded_on >= timezone.now() - datetime.timedelta(days=1)
    class Meta:
        verbose_name_plural = "Downloading"

class Watch_history(models.Model):
    user = models.CharField(max_length=100)
    ip = models.TextField()
    title_long = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.user
    class Meta:
        verbose_name_plural = "History"
