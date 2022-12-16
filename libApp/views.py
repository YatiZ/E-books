from django.shortcuts import render,redirect,HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from .models import Person,Book
from django.views import View
from django.contrib.auth.models import User
from .forms import book_form,RegistrationForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,  DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

from django.template.loader import render_to_string
# Create your views here.

#Registration
# def login(request):
#     return render(request,'account/login.html')
def profile(request):
    user = User.objects.get(username = request.user)
    books = Book.objects.all()
    return render(request,'account/profile.html',{'user':user,'book':books})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.clean_username['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            email_subject = 'Activate your account'
            uidb64 = force_bytes(urlsafe_base64_encode(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs = {'uidb64':uidb64,'token':token_generator.make_token(user)})
            activate_url = 'http://'+domain+link
            email_body = 'Hi' + user.username+ 'please use this link to verify your account\n'+activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com'
                [email],
            )
            email.send(fail_silently= False)
            messages.success(request,'Account successfully created')
            return render(request,'account/register.html')

            # current_site =get_current_site(request)
            # subject = 'Activate Your Account'
            # message = render_to_string('account/activation_email.html',{
            #     'user': user,
            #     'domain':current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject=subject, message = message)
            # return HttpResponse('registered successfully and activation sent')
    else:
        form = RegistrationForm()
    return render(request,'account/register.html',{'form':form})

class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('login')

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


