from django.urls import path
from .import views
from .views import VerificationView 
from django.contrib.auth import views as auth_views
from.forms import UserLoginForm

urlpatterns = [ 
    # path('login',auth_views.LoginView.as_view( template_name = "account/login.html", authentication_form = UserLoginForm),name = 'login'),
    # path('',views.login_form, name = 'login-form'),
    # path('logout',auth_views.LogoutView.as_view(template_name = 'account/logout.html'),name ='logout'),
    path('login/',views.loginView, name='login'),
    
    path('logout',views.logoutView,name='logout'),
    path('register/',views.register,name = 'register'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name= 'activate'),
    path('create',views.create_acc,name='create'),

    #user
    path('profile/<str:pk>',views.profile,name='profile'),
    path('index/',views.index,name='index'),
    # path('user_home/',views.user_home,name='user_home'),
    path('user_style/<str:pk>',views.user_style,name='user_style'),
    path('all-book',views.all_book,name='all-book'),
    path('setting/',views.setting,name='setting'),

    #librarian
    path('style/',views.style,name='style'),
    path('home/',views.home,name='home'),
    path('userlist/',views.user_list,name = 'userlist'),
    path('addbook/',views.add_book,name='addbook'),
    path('delete/<str:pk>',views.delete_book,name='delete'),
    path('update/<str:pk>',views.update_book,name='update'),
    path('library/',views.index_lib,name='index_lib'),
]