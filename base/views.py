from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Question, Answers, Likes
from .forms import AskQuestionForm, WriteCommentForm
# Create your views here.

class HomeView(View):
    """Handles rendering the home page.
    This view retrieves all questions and renders the home page with the question's title.

    Args:
        View (class): Django in build class for handling methods.
    """
    def get(self, request):
        """Handles GET requests to display the home page.
        Retrieves all questions from the database and renders the home page template with the questions.

        Args:
            request (request): Django request argument.

        Returns:
            template: It renders home page with all questions.
        """
        questions = Question.objects.only('id', 'title')
        return render(request, 'base/index.html', context={'questions': questions})
    

class QuestionView(View):
    """Handles displaying a question and its answers.

    This view retrieves a specific question and its associated answers, renders the question page,
    and handles POST requests to submit new answers.

    Args:
        View (class): Django in build class for handling methods.
    """
    def get(self, request, ids):
        """Handles GET requests to display a question and its answers.

        Retrieves the question and its answers from the database, and renders the question template.

        Args:
            request (request): Django request argument.
            ids (int): id of question.

        Returns:
            template: It renders question page with question and its answers.
        """
        form = WriteCommentForm()
        question = Question.objects.prefetch_related('question_answers').filter(id=ids)
        return render(request, 'base/pages/questions.html', context={'question': question, 'form': form})
    
    @method_decorator(login_required)
    def post(self, request, ids):
        """Handles POST requests to submit a new answer to a question.

        Retrieves the question, processes the submitted answer form, creates a new answer
        associated with the current user and question, and redirects back to the question page.

        Args:
            request (request): Django request argument.
            ids (int): id of question.

        Returns:
            redirect: redirect to question page.
        """
        question = Question.objects.filter(id=ids).first()
        comment = WriteCommentForm(request.POST)
        if comment.is_valid():
            answer = comment.cleaned_data['answer']
            Answers.objects.create(
                user=request.user,
                question=question,
                answer=answer
            )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@method_decorator(login_required, name='dispatch')    
class AskQuestionView(View):
    """Handles asking new questions.

    This view renders the ask question form and processes POST requests to create new questions.
    It then redirects to the newly created question's page.

    Args:
        View (class): Django in build class for handling methods.
    """
    def get(self, request):
        """Handles GET requests to display the ask question form.

        Renders the ask question template with an empty form.

        Args:
            request (request): Django request argument.

        Returns:
            template: It renders ask question page with an empty form.
        """
        form = AskQuestionForm()
        return render(request, 'base/pages/ask_question.html', {'form' : form})
    
    def post(self, request):
        """Handles POST requests to create a new question.

        Retrieves the question title from the form, creates a new question
        associated with the current user, and redirects to the question page.


        Args:
            request (request): Django request argument.

        Returns:
            redirect: redirect to question page.
        """
        question_id = []
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            question = Question.objects.create(
                user=request.user,
                title=title
            )
            question_id.append(question.id)
        return HttpResponseRedirect(f'/question/{question_id[0]}/')

class LikeView(View):
    """Handles like and unlike answers.

    This view manages the process of like and unlike answers, handling POST requests.
    It toggles the like status of an answer for the current user.

    Args:
        View (class): Django in build class for handling methods.

    Returns:
        redirect: redirect to previous page.
    """
    @method_decorator(login_required)
    def post(self, request):
        """Handles POST requests to like or unlike an answer.

        Retrieves the answer ID from the request, toggles the like status for the
        current user, and redirects back to the previous page.

        Args:
            request (request): Django request argument.

        Returns:
            redirect: redirect to previous page.
        """
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