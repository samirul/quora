from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Question, Answers, Likes
# Create your views here.

class HomeView(View):
    def get(self, request):
        questions = Question.objects.only('id', 'title')
        return render(request, 'base/index.html', context={'questions': questions})
    

class QuestionView(View):
    def get(self, request, ids):
        question = Question.objects.prefetch_related('question_answers').filter(id=ids)
        return render(request, 'base/pages/questions.html', context={'question': question})
    
    @method_decorator(login_required)
    def post(self, request, ids):
        question = Question.objects.filter(id=ids).first()
        comment = request.POST.get('form-input-text-box')
        if not comment:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        Answers.objects.create(
            user=request.user,
            question=question,
            answer=comment
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class AskQuestionView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'base/pages/ask_question.html')
    
    @method_decorator(login_required)
    def post(self, request):
        title = request.POST.get('form-input-text-new-question')
        question = Question.objects.create(
            user=request.user,
            title=title
        )
        return HttpResponseRedirect(f'/question/{question.id}/')

class LikeView(View):
    def post(self, request):
        ids = request.POST.get('answer_id')
        answer = Answers.objects.get(id=ids)
        if request.user in answer.liked.all():
            answer.liked.remove(request.user)
        else:
            answer.liked.add(request.user)
        
        like, created = Likes.objects.get_or_create(
            user=request.user,
            answer=answer
        )
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))