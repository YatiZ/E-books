from django import forms
from .models import Book
class book_form(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('book_name','author','book_types','book_cover','book_pdf')
