from django.shortcuts import render, redirect, HttpResponse
from api.models import Books

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def create(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'create.html')

def manage_download(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'downloads.html')

def upload(request):

    if request.method == 'POST':

        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        description = request.POST['description']
        file = request.FILES['file']

        book = Books(
            title=title,
            author=author,
            price=price,
            description=description,
            file=file
        )

        book.save()

        return HttpResponse('Uploaded Successfully')

def manage(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'manage.html')

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'dashboard.html')