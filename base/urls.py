
from django.urls import path
from .views import HomeView, QuestionView, AskQuestionView, LikeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("question/<str:ids>/", QuestionView.as_view(), name="question"),
    path("new-question/new/", AskQuestionView.as_view(), name="new-question"),
    path("like/", LikeView.as_view(), name="like"),
]