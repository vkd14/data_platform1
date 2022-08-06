from django.db import models

# Create your models here.

class Resource(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    location = models.CharField(max_length=255)
    dataset_name = models.CharField(max_length=255)

class Dataset(models.Model):
    name = models.CharField(primary_key=True, max_length=255, editable=False)
    tags = models.CharField(max_length=255)
    description = models.CharField(max_length=255)