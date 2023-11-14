from django.contrib import admin

# Register your models here.
from .models import Books, Download

admin.site.register(Books)
admin.site.register(Download)
