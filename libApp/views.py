from django.shortcuts import render,redirect,HttpResponse
from .models import Person,Book
from .forms import book_form
# Create your views here.

#User Views
def user_style(request):
    return render(request,'user/style.html')

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        person_data = Person.objects.create(name=name,gender = gender)
        person_data.save()
        return redirect('home')
    return render(request,'user/index.html')

def user_home(request):
    user = Person.objects.all()
    books = Book.objects.all()
    # num_visits = request.session.get('num_visits',0)
    # request.session['num_visits'] = num_visits + 1

    return render(request,'user/home.html',{'user':user,'books':books})



#Librarian View
def add_book(request):
    if request.method == 'POST':
        book_name = request.POST['book_name']
        author = request.POST['author']
        book_types = request.POST['book_types']
        cover = request.FILES.get('cover')
        pdf = request.FILES.get('pdf')
        adding_book = Book.objects.create(book_name=book_name,author=author,book_types=book_types,book_cover = cover,book_pdf = pdf)
        adding_book.save()
        return redirect('home')
    return render(request,'librarian/addbook.html')

def delete_book(request,pk):
    del_book = Book.objects.get(book_id = pk)
    del_book.delete()
    return redirect('home')

def update_book(request,pk):
    edit_book = Book.objects.get(book_id = pk)
    books = book_form(request.POST or None, instance=edit_book)
    if books.is_valid():
        books.save()
        return redirect('home')
    return render(request,'librarian/update.html',{'edit':edit_book,'books':books})

def style(request):
    books = Book.objects.all()
    return render(request,'librarian/style.html',{'books':books})

def home(request):
    books = Book.objects.all()
    return render(request,'librarian/home.html',{'books':books})

def user_list(request):
    lists = Person.objects.all()
    return render(request,'librarian/user_list.html',{'lists':lists})

def index_lib(request):
    return render(request,'librarian/index.html')

def all_book(request):
    books = Book.objects.all()
    return render(request,'user/all_book.html',{'books':books})


