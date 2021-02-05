from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login_main),  # main: before/after login
    path('auth/', auth_views.LoginView.as_view(template_name='login/login_page.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('select/', views.login_select, name='login_select'),
]
