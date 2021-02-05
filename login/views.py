from django.shortcuts import render


def login_main(request):
    return render(request, 'login/login_base.html')


def login_select(request):
    return render(request, 'login/login_select.html')
