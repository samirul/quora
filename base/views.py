from django.shortcuts import render
from django.views import View
from .models import Question, Answers
# Create your views here.

class HomeView(View):
    def get(self, request):
        questions = Question.objects.only('id', 'title')
        return render(request, 'base/index.html', context={'user': request.user, 'questions': questions})