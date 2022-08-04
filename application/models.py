from django.db import models

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(primary_key=True, max_length=255, editable=False)
    tags = models.CharField(max_length=255)
    description = models.CharField(max_length=500)

class Resource(models.Model):
    name = models.CharField(primary_key = True, max_length=255)
    location = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)