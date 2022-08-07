from django.db import models


# Create your models here.

class Resource(models.Model):
    """This model is for the Resource file associated with the Datasets table. There can be multiple
    Resources for a single Dataset.
    """
    name = models.CharField(primary_key=True, max_length=255)  # name of the resource file
    location = models.CharField(max_length=255)  # location of the resource file in the file system
    dataset_name = models.CharField(max_length=255)  # name of the dataset to which the Resource file belongs


class Dataset(models.Model):
    """ This model is for the Dataset information. It can store details like name, tags and description regarding
    the dataset.
    """
    name = models.CharField(primary_key=True, max_length=255, editable=False)  # name of the dataset
    tags = models.CharField(max_length=255)  # tags associated with that dataset
    description = models.CharField(max_length=255)  # description for the dataset
