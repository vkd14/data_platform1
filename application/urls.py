from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path("allDataset/",views.all_dataset), 
    path("uploadDataset/", views.UploadFileView.as_view(), name='upload_dataset'), 
    path("fetchDataset/<str:dataset_name>", views.fetch_dataset),
    path("fetchDatasetDetail/<str:dataset_name>", views.fetch_dataset_detail),
    path("getResource/<str:dataset_name>", views.get_resorce_data)
    ]