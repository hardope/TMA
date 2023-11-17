from django.urls import path
from .views import *

urlpatterns = [
    path('', welcome),
    path('books/', BooksView.as_view()),
    path('books/<str:pk>/', OneBook.as_view()),
    path('download/', DownloadView.as_view()),
    path('download/<str:link>/', download),
    path('auth/', Auth.as_view()),
]