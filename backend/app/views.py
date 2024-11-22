from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import TemplateView

def home(request):
    return render(request, 'home.html')
    
def logout_confirm(request):
    return render(request, 'logout_confirm.html')

def login(request):
    return render(request, 'login.html')


from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options']