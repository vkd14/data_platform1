from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path("allDataset/", views.all_dataset),
    # to get the details of all the Datasets present in the database.
    path("uploadDataset/", views.UploadFileView.as_view(), name='upload_dataset'),
    # to upload a dataset
    path("fetchDatasetDetail/<str:dataset_name>", views.fetch_dataset_detail),
    # to get the metadata of a particular dataset
    path("getResource/<str:dataset_name>", views.get_resource_data)
    # to download the resource files associated with a particular dataset
]
