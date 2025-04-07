
from django.urls import path
from .views import HomeView, QuestionView, AskQuestionView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("question/<str:ids>/", QuestionView.as_view(), name="question"),
    path("new-question/new/", AskQuestionView.as_view(), name="new-question"),
]