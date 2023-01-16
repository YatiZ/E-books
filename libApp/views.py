from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import Person,Book
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import book_form,RegistrationForm
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,  DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth import authenticate,logout
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import BookSerializer
from rest_framework import generics
# Create your views here.

#Registration
# def login_form(request):
#     return render(request,'account/login.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_staff:
                return redirect('home')
            else:
                return redirect('/profile/'+username)
        return redirect('/profile/'+username)
    return render(request,'account/login.html')


def logoutView(request):
    logout(request)
    return redirect('login')

def profile(request,pk):
    user = User.objects.get(username = pk)
    books = Book.objects.all()
    return render(request,'user/home.html',{'books':books,'user':user})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Account was created successfully')
            return redirect('profile')
    else:
        form = RegistrationForm()
        
    return render(request,'account/register.html',{'form':form})

def create_acc(request):
    return render(request,'account/create_acc.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.email = form.clean_username['email']
#             user.set_password(form.cleaned_data['password'])
#             user.is_active = False
#             user.save()
#             email_subject = 'Activate your account'
#             uidb64 = force_bytes(urlsafe_base64_encode(user.pk))
#             domain = get_current_site(request).domain
#             link = reverse('activate',kwargs = {'uidb64':uidb64,'token':token_generator.make_token(user)})
#             activate_url = 'http://'+domain+link
#             email_body = 'Hi' + user.username+ 'please use this link to verify your account\n'+activate_url
#             email = EmailMessage(
#                 email_subject,
#                 email_body,
#                 'noreply@semycolon.com'
#                 [email],
#             )
#             email.send(fail_silently= False)
#             messages.success(request,'Account successfully created')
#             return render(request,'account/register.html')

#     else:
#         form = RegistrationForm()
#     return render(request,'account/register.html',{'form':form})

class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('login')

#User Views
def user_style(request,pk):
    user = User.objects.get(username = pk)
    return render(request,'user/style.html',{'user':user})

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        person_data = Person.objects.create(name=name,gender = gender)
        person_data.save()
        return redirect('home')
    return render(request,'user/index.html')

# def user_home(request):
#     user = Person.objects.all()
#     books = Book.objects.all()
#     # num_visits = request.session.get('num_visits',0)
#     # request.session['num_visits'] = num_visits + 1

#     return render(request,'user/home.html',{'user':user,'books':books})


def setting(request):
    user = User.objects.all()
    return render(request,'user/setting.html',{'user':user})

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
    users = User.objects.all()
    return render(request,'librarian/user_list.html',{'lists':lists,'users':users})

def index_lib(request):
    book = Book.objects.all()
    total_book = len(book)
    users = User.objects.all()
    total_user = len(users)
    return render(request,'librarian/index.html',{'book':book,'total_book':total_book,'total_user':total_user})

def all_book(request):
    return HttpResponse('hello')
    user = User.objects.get(username =request.user.username)
    
    books = Book.objects.all()
    return render(request,'user/all_book.html',{'books':books})

@api_view(['GET','POST'])
def book(request,pk=None,*args,**kwargs ):
    method = request.method
    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Book,pk = pk)
            data = BookSerializer(obj, many = False).data
            return Response(data)
        queryset = Book.objects.all()
        data = BookSerializer(queryset,many=True).data
        return Response(data)
    
    if method == "POST":

        serializer = BookSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
        return Response({'invalid':'No good data'},status=400)
    
    
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
book_list_view = BookListView.as_view()

@api_view(['GET'])
def one_book(request,pk):
    book = Book.objects.get(book_id = pk)
    serializer = BookSerializer(book,many = False)
    return Response(serializer.data)

@api_view(['POST'])
def bookupdate(request,pk):
    book = Book.objects.get(book_id=pk)
    serializer = BookSerializer(instance=book,data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def bookdelete(request,pk):
    book = Book.objects.get(book_id = pk)
    book.delete()
    return Response("Item successfully deleted!")