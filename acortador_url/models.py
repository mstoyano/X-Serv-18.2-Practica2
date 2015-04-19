from django.db import models

# Create your models here.
class url_type(models.Model):
	large_url = models.CharField(max_length=32)
	short_url = models.CharField(max_length=32)