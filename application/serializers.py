from rest_framework import serializers


# remember to import the File model
class FileUploadSerializer(serializers.Serializer):
    dataset_name = serializers.CharField(max_length=255)
    file = serializers.FileField()
    description = serializers.CharField(max_length=255)
