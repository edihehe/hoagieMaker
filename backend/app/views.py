from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')

def logout(request):
    return render(request, 'logout.html')

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options']