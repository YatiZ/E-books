from django.urls import path
from .import views

urlpatterns = [ 
    #user
    path('index/',views.index,name='index'),
    path('user_home/',views.user_home,name='user_home'),
    path('user_style',views.user_style,name='user_style'),
    path('all-book',views.all_book,name='all-book'),


    #librarian
    path('style/',views.style,name='style'),
    path('home/',views.home,name='home'),
    path('userlist/',views.user_list,name = 'userlist'),
    path('addbook/',views.add_book,name='addbook'),
    path('delete/<str:pk>',views.delete_book,name='delete'),
    path('update/<str:pk>',views.update_book,name='update'),
    path('library/',views.index_lib,name='index_lib'),
]