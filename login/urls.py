from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login_main),
    path('login/', auth_views.LoginView.as_view(template_name='login/login_base.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('select/', views.login_select, name='login_select'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('settings/nickname/', views.nickname, name='nickname'),
    path('settings/personal_inf/',
         views.personal_inf, name='personal_inf'),
]
