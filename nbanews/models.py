from django.db import models

# Create your models here.
class NbaNews(models.Model):
   url = models.URLField(default='', max_length=1000, unique=True)
   title = models.CharField(default='', max_length=1000)
   imgsrc = models.URLField(default='', max_length=1000)
   creator = models.CharField(default='', max_length=100)
   post_time = models.DateTimeField()
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.title