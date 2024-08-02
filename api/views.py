from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class Auth(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="Create a Book",
        responses={
            200: 'OK',
        }
    )

    def post(self, request):

        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response(
                {'message': 'Invalid Data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {'message': 'Invalid Credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class BooksView(APIView):

    authentication_classes = []

    @swagger_auto_schema(
        operation_description="Get All Books",
        responses={
            200: BooksSerializer(many=True)
        }
    )
    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a Book",
        request_body=BooksSerializer,
        responses={
            201: BooksSerializer
        }
    )
    def post(self, request):

        if not request.user.is_authenticated:

            return Response({'message': 'You are not authorized to perform this action.'})

        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(
            {'message': 'Invalid Data'},
            status=status.HTTP_400_BAD_REQUEST
        )

class OneBook(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a Book",
        responses={
            200: BooksSerializer
        }
    )
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BooksSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a Book",
        request_body=BooksSerializer,
        responses={
            200: BooksSerializer
        }
    )
    def put(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BooksSerializer(book, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(
            {'message': 'Invalid Data'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Delete a Book",
        responses={
            204: 'No Content'
        }
    )
    def delete(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DownloadView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get All Downloads",
        responses={
            200: DownloadSerializer(many=True)
        }
    )
    def get(self, request):
        downloads = Download.objects.all()
        serializer = DownloadSerializer(downloads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a Download",
        request_body=DownloadSerializer,
        responses={
            201: DownloadSerializer
        }
    )
    def post(self, request):
        serializer = DownloadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        operation_description="Update a Download",
        request_body=DownloadSerializer,
        responses={
            200: DownloadSerializer
        }
    )

    def put(self, request):
        data = request.data
        new_data = {}
        new_data['limit'] = request.data['limit']
        download = Download.objects.get(pk=data['id'])
        serializer = DownloadSerializer(download, data=new_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Invalid Data'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        operation_description="Delete a Download",
        responses={
            204: 'No Content'
        }
    )

    def delete(self, request):
        download = Download.objects.get(pk=request.data['id'])
        download.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def download(request, link):
    try:
        download = get_object_or_404(Download, id=link)
    except:
        return HttpResponse("<h1>Download Link Expired or Invalid</h1>")

    if download.count >= download.limit:
        return HttpResponse("<h1>Download Limit Exceeded</h1>")

    expiration_time = download.created_at + timezone.timedelta(days=1)
    if expiration_time < timezone.now():
        return HttpResponse("<h1>Download Link Expired</h1>")
    
    download.count += 1
    download.save()

    file_path = download.book.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + download.book.title + '.pdf'

    return response

def welcome(request):
    return JsonResponse({'message': 'Welcome to TMA API'})