from typing import Any
from django.db import models
from uuid import uuid4

# Create your models here.

def books_upload_to(instance, filename):
    return f'books/{uuid4()}.{filename.split(".")[-1]}'

class Books(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(blank=False)
    file = models.FileField(upload_to=books_upload_to)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'books'
        verbose_name = 'book'
        verbose_name_plural = 'books'

class Download(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    limit = models.IntegerField(default=2)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.name} - {self.book.title}'
    
    class Meta:
        db_table = 'download'
        verbose_name = 'download'
        verbose_name_plural = 'downloads'
