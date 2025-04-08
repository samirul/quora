from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User
# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'base/authentication/login.html')
    
class RegisterView(View):
    def get(self, request):
        return render(request, 'base/authentication/register.html')
    
    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists.")
                return HttpResponseRedirect('/auth/register/')
            
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists.")
                return HttpResponseRedirect('/auth/register/')
            
            if password != confirm_password:
                messages.info(request, "Passwords do not match.")
                return HttpResponseRedirect('/auth/register/')
            
            validate_password(password=password)
            
            user= User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Registration Successful.")

            return HttpResponseRedirect('/auth/login/')
    
        except ValidationError as e:
            messages.info(request, f"{e.messages[0]}")
            return HttpResponseRedirect('/auth/register/')