from rest_framework.serializers import ModelSerializer
from .models import *

class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class DownloadSerializer(ModelSerializer):
    class Meta:
        model = Download
        fields = '__all__'