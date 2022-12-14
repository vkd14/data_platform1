import codecs
import csv
import os.path
import zipfile
from io import BytesIO
from django.db import connection
from django.http import HttpResponse
from application.models import Dataset, Resource


def all_dataset():
    datasets = Dataset.objects.raw('SELECT name FROM application_dataset')
    return datasets


def make_csv(dataset_name, count, resource_file, description):
    RESOURCE_SUFFIX = "_resource_file.csv"
    cursor = connection.cursor()
    csvreader = csv.reader(codecs.iterdecode(resource_file, 'utf-8'))
    tags = str(next(csvreader))
    location = f"/Users/thev/Desktop/data_platform/application/resource/{dataset_name + str(count) + RESOURCE_SUFFIX}"
    with open(location, 'wb+') as destination:
        for chunk in resource_file.chunks():
            destination.write(chunk)
    print(fr"{location}", fr"{tags}")
    return location, tags


def upload_dataset(dataset_name, resource_file, description):
    count = Dataset.objects.filter(name=dataset_name).count()
    if not count:
        location, tags = make_csv(dataset_name, count, resource_file, description)
        Dataset.objects.create(name=dataset_name, tags=tags, description=description)
        Resource.objects.create(name=os.path.basename(location), location=location, dataset_name=dataset_name)

    else:
        res_count = Resource.objects.filter(dataset_name=dataset_name).count()
        location, tags = make_csv(dataset_name, res_count, resource_file, description)
        Resource.objects.create(name=os.path.basename(location), location=location, dataset_name=dataset_name)


def fetch_dataset_details(dataset_name):
    dataset = Dataset.objects.raw("SELECT * FROM application_dataset WHERE name= %s", [dataset_name])
    return dataset


def getfiles(dataset_name):
    filenames = []
    results = Resource.objects.raw('SELECT * FROM application_resource WHERE dataset_name = %s', [dataset_name])
    for record in results:
        filenames.append(record.location)
    zip_subdir = f"/"
    zip_filename = "%s.zip" % dataset_name
    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

    zf.close()

    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp
