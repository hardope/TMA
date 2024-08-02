from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login/', login),
    path('create/', create),
    path('upload/', upload),
    path('manage/', manage),
    path('downloads/', manage_download),
    path('dashboard', dashboard)
]