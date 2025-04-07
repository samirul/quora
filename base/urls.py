
from django.urls import path
from .views import HomeView, QuestionView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("question/<str:ids>/", QuestionView.as_view(), name="question"),
]