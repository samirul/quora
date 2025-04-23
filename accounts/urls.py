from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name='base/authentication/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]