import csv
import codecs
from os import path
from application.models import Dataset
from django.db import connection

def all_dataset():
    datasets = Dataset.objects.raw('SELECT name FROM application_dataset')
    return datasets

def upload_dataset(dataset_name, resource_file, description):
    RESOURCE_SUFFIX = "_resource_file.csv"
    cursor = connection.cursor()
    csvreader = csv.reader(codecs.iterdecode(resource_file,'utf-8'))
    tags = str(next(csvreader))
    location = f"/Users/thev/Desktop/data_platform/application/resource/{dataset_name+RESOURCE_SUFFIX}"
    with open(location,'wb+') as destination:
        for chunk in resource_file.chunks():
            destination.write(chunk)
    print(fr"{location}",fr"{tags}")
    #cursor.execute(f'INSERT INTO application_resource VALUES ({dataset_name+RESOURCE_SUFFIX},{location},{description})')
    cursor.execute(f'INSERT INTO application_dataset VALUES ({dataset_name},tags,{description})')

def fetch_dataset_details(dataset_name):
    dataset = Dataset.objects.raw(f'SELECT * FROM application_dataset WHERE name={dataset_name}')
    return dataset