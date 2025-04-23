from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import RegisterForm

class RegisterView(View):
    """"View for user registration.

    Args:
        View (class): Django in build class for handling methods.
    """
    def get(self, request):
        """Handles GET requests to the login page.
        Renders the login template.

        Args:
            request: The incoming HTTP request.

        Returns:
            template: A rendered HTML response for the registration page with an empty form.
        """
        form = RegisterForm()
        return render(request, 'base/authentication/register.html', {'form': form})
    
    def post(self, request):
        """Handles POST requests to the registration page.

        Validates the submitted form, saves the new user if valid, and redirects to the login page.
        If the form is invalid, displays an error message and redirects back to the registration page.

        Args:
            request: The incoming HTTP request.

        Returns:
            An HTTP redirect response.
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, "Registration Successful.")
            form.save()
            return HttpResponseRedirect('/auth/login/')
        messages.info(request, "Something is wrong, please try again.")
        return HttpResponseRedirect('/auth/register/')
    

# class LoginView(View):
#     def get(self, request):
#         return render(request, 'base/authentication/login.html')
