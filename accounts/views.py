from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from .models import User
# Create your views here.
         
class RegisterView(View):
    """Handles user registration.
    This view manages the user registration process, handling both GET and POST requests.
    It validates user inputs, creates new user accounts, and redirects upon successful registration.

    Args:
        View (class): Django in build class for handling methods.
    """
    def get(self, request):
        """Handles GET requests to display the registration form.

        If the user is already authenticated, redirects to the home page.
        Otherwise, renders the registration template.

        Args:
            request (request): Django request argument.

        Returns:
            template: It renders register html page.
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, 'base/authentication/register.html')
    
    def post(self, request):
        """Handles POST requests to process registration data.

        Retrieves user inputs, validates them, creates a new user account,
        and redirects to the login page upon successful registration.
        Handles validation errors and redirects back to the registration page if necessary.
        

        Args:
            request (request): Django request argument.

        Returns:
            redirect: redirect to login page if successful else will redirect
            back to register page.
        """
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
        

class LoginView(View):
    def get(self, request):
        next_url = request.GET.get('next', '/')
        if request.user.is_authenticated:
            return HttpResponseRedirect(next_url)
        return render(request, 'base/authentication/login.html', {'next': next_url})
    
    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            next_url = request.POST.get('next') or request.GET.get('next', '/')
            
            if not email or not password:
                messages.info(request, "Please provide all details.")
                
            if not User.objects.filter(email=email).exists():
             messages.info(request, "Email isn't Registered, Please Register Your Account First.")
             return HttpResponseRedirect('/auth/login/')
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful.")
                return HttpResponseRedirect(next_url)
            messages.info(request, "Invalid Credentials.")
            return HttpResponseRedirect('/auth/login/')
        
        except Exception as e:
            messages.info(request, f"Something is wrong: {str(e)}")
            return HttpResponseRedirect('/auth/login/')
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout Successful.")
        return HttpResponseRedirect('/auth/login/')