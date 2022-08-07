import codecs
import csv
import mimetypes
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
    # check_record = Dataset.objects.raw('SELECT COUNT(*) FROM application_dataset WHERE name= %s', [dataset_name])
    # count = check_record[0]

    # cursor.execute(f'INSERT INTO application_resource VALUES ({dataset_name+RESOURCE_SUFFIX},{location},{dataset_name})')
    # cursor.execute(f'INSERT INTO application_dataset VALUES ({dataset_name},tags,{description})')
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


def fetch_dataset(dataset_name):
    # Define Django project base directory
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # filename = 'test.txt'
    # Define the full file path
    # RESOURCE_SUFFIX = "_resource_file.csv"
    # dataset_name = "abc.csv"
    # results = Resource.objects.raw('SELECT * FROM application_resource WHERE dataset_name = %s', [dataset_name])
    # for record in results:
    #     print(record.location)
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



def getfiles(dataset_name):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    # filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]
    filenames = []
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    results = Resource.objects.raw('SELECT * FROM application_resource WHERE dataset_name = %s', [dataset_name])
    for record in results:
        filenames.append(record.location)
    zip_subdir = f"/"
    zip_filename = "%s.zip" % dataset_name

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

