from django.db import models

# Create your models here.

class Link(models.del):
    url = models.URLField()
    description = models.TextField(blank=True)