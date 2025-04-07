from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .models import Question, Answers
# Create your views here.

class HomeView(View):
    def get(self, request):
        questions = Question.objects.only('id', 'title')
        return render(request, 'base/index.html', context={'user': request.user, 'questions': questions})
    

class QuestionView(View):
    def get(self, request, ids):
        question = Question.objects.prefetch_related('question_answers').filter(id=ids)
        return render(request, 'base/pages/questions.html', context={'user': request.user, 'question': question})
    
    def post(self, request, ids):
        question = Question.objects.filter(id=ids).first()
        comment = request.POST.get('form-input-text-box')
        Answers.objects.create(
            user=request.user,
            question=question,
            answer=comment
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
