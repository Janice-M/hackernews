from django.db import models

# Create your models here.

class link(models.Model):
    url=models.URLField()
    description = models.TextField(blank=True)
