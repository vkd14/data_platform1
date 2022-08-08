from django.http import HttpResponse
from rest_framework import generics
from . import query
from . import serializers


# Create your views here.
def all_dataset(request):
    dataset_names = []
    datasets = query.all_dataset()
    if datasets:
        for dataset in datasets:
            dataset_names.append(str(dataset.name))
        return HttpResponse(f"Datasets List : {dataset_names}")
    else:
        return HttpResponse("No Datasets to Return!")


def fetch_dataset_detail(request, dataset_name):
    dataset = query.fetch_dataset_details(dataset_name)
    return HttpResponse(f'name = {dataset[0].name},tags = {dataset[0].tags}, description = {dataset[0].description}')


def get_resource_data(request, dataset_name):
    return query.getfiles(dataset_name)


class UploadFileView(generics.CreateAPIView):
    serializer_class = serializers.FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        dataset_name = serializer.validated_data['dataset_name']
        description = serializer.validated_data['description']
        print(f"{dataset_name},{description}")
        query.upload_dataset(dataset_name, file, description)
        return HttpResponse("Upload Successful!!")
