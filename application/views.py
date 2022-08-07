from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from application import serializers
from . import query
from . import serializers
from . import models
from django.http import HttpResponseRedirect




# Create your views here.
def all_dataset(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    dataset_names = []
    datasets = query.all_dataset()
    if datasets:
        for dataset in datasets:
            dataset_names.append(str(dataset.name))
        return HttpResponse(f"Datasets List : {dataset_names}")
    else:
        return HttpResponse("No Datasets to Return!")
  


# def upload_dataset(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         print(f"Form Data -> {request.FILES}")
#         if form.is_valid():
#             #query.upload_dataset(request.FILES['dataset_name'],request.FILES['file'],request.FILES['description'])
#             query.upload_dataset(request.FILES['dataset_name'],request.FILES['file'])
#             return HttpResponse("Upload Successfull!")
#         else:
#             return HttpResponse("Upload Error")
#     else:
#         form = UploadFileForm()
# def fetch_dataset(request):
#     return HttpResponse("Fetch Data")

def fetch_dataset(request, dataset_name):
    """_summary_

    Args:
        request (_type_): _description_
        dataset_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    return HttpResponse(query.fetch_dataset(dataset_name))


def fetch_dataset_detail(request, dataset_name):
    """_summary_

    Args:
        request (_type_): _description_
        dataset_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    dataset = query.fetch_dataset_details(dataset_name)
    return HttpResponse(f'name = {dataset[0].name},tags = {dataset[0].tags}, description = {dataset[0].description}')

def get_resorce_data(request, dataset_name):
    """_summary_

    Args:
        request (_type_): _description_
        dataset_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (query.getfiles(dataset_name))

class UploadFileView(generics.CreateAPIView):
    """_summary_

    Args:
        generics (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = serializers.FileUploadSerializer

    def post(self, request, *args, **kwargs):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        dataset_name = serializer.validated_data['dataset_name']
        description = serializer.validated_data['description']
        print(f"{dataset_name},{description}")
        query.upload_dataset(dataset_name, file, description)
        return HttpResponse("Upload Succesful!!")
