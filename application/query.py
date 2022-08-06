import csv
import codecs
import mimetypes
import os.path
from os import path

from django.http import HttpResponse

from application.models import Dataset, Resource
from django.db import connection


def all_dataset():
    datasets = Dataset.objects.raw('SELECT name FROM application_dataset')
    return datasets


def upload_dataset(dataset_name, resource_file, description):
    RESOURCE_SUFFIX = "_resource_file.csv"
    cursor = connection.cursor()
    csvreader = csv.reader(codecs.iterdecode(resource_file, 'utf-8'))
    tags = str(next(csvreader))
    location = f"/Users/thev/Desktop/data_platform/application/resource/{dataset_name + RESOURCE_SUFFIX}"
    with open(location, 'wb+') as destination:
        for chunk in resource_file.chunks():
            destination.write(chunk)
    print(fr"{location}", fr"{tags}")
    Dataset.objects.create(name=dataset_name, tags=tags, description=description)
    Resource.objects.create(name=os.path.basename(location), location=location, dataset_name=dataset_name)
    # cursor.execute(f'INSERT INTO application_resource VALUES ({dataset_name+RESOURCE_SUFFIX},{location},{dataset_name})')
    #cursor.execute(f'INSERT INTO application_dataset VALUES ({dataset_name},tags,{description})')


def fetch_dataset_details(dataset_name):
    dataset = Dataset.objects.raw("SELECT * FROM application_dataset WHERE name= %s", [dataset_name])
    return dataset


def fetch_dataset(dataset_name):
    # Define Django project base directory
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # filename = 'test.txt'
    # Define the full file path
    # RESOURCE_SUFFIX = "_resource_file.csv"
    # dataset_name = "abc.csv"
    filepath = f"/Users/thev/Desktop/data_platform/application/resource/{dataset_name}"
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; dataset_name=%s" % dataset_name
    # Return the response value
    return response

if __name__ == "__main__":
    fetch_dataset("abc.csv")
