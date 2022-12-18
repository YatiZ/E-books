from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)
    gender_choices = (
        ('Male','Male'),
        ('Female','Female'),
    )
    gender = models.CharField(max_length=100,choices=gender_choices)

    def person(self):
        return f"{self.name}{self.gender}"


    def __str__(self):
        return self.person()

class Book(models.Model):
    book_id = models.BigAutoField(primary_key=True)
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    books = (
        ('Education','education'),
        ('Mangas','mangas'),
        ('MM_Books','mm_books'),
        ('History','history'),
        ('Health','health'),
        ('Novel','novel')
    )
    book_types = models.CharField(max_length=200,choices=books)
    date = models.DateField(auto_now=True)
    book_cover = models.ImageField(upload_to='covers')
    book_pdf = models.FileField(upload_to='pdfs')

    def __str__(self):
        return self.book_name

class Post(models.Model):
    title = models.CharField(max_length=100,unique=True)
    num_visits = models.IntegerField(default=0)

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    

     

   
