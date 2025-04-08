from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Question, Answers, Likes
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
    """Handles displaying a specific question and its answers.

    This view retrieves a question by its ID, along with its related answers,
    and renders the question page. It also handles POST requests for adding new answers.

    Args:
        View (class): Django in build class for handling methods.
    """
    def get(self, request, ids):
        """Handles GET requests to display a specific question and its answers.

        Retrieves the question from the database based on the provided ID,
        prefetches related answers, and renders the question template.

        Args:
            request (request): Django request argument.
            ids (int): question id.
        Returns:
            template: It renders question page with answers.
        """
        question = Question.objects.prefetch_related('question_answers').filter(id=ids)
        return render(request, 'base/pages/questions.html', context={'question': question})
    
    @method_decorator(login_required)
    def post(self, request, ids):
        """Handles POST requests to add a new answer to a question.

        Retrieves the question by ID, creates a new answer associated with the
        current user and question, and redirects back to the question page.

        Args:
            request (request): Django request argument.
            ids (int): question id.

        Returns:
            redirect: redirect to question page.
        """
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
    """Handles asking new questions.

    This view manages the process of asking new questions, handling both GET and POST requests.
    It renders the ask question page and creates new question entries in the database.

    Args:
         View (class): Django in build class for handling methods.

    Returns:
        template: It renders ask question page for new question.
    """
    @method_decorator(login_required)
    def get(self, request):
        """Handles GET requests to display the ask question form.

        Renders the ask question template.

        Args:
             request (request): Django request argument.

        Returns:
             template: It renders ask question page.
        """
        return render(request, 'base/pages/ask_question.html')
    
    @method_decorator(login_required)
    def post(self, request):
        """Handles POST requests to create a new question.

        Retrieves the question title from the request, creates a new question
        associated with the current user, and redirects to the question page.


        Args:
            request (request): Django request argument.

        Returns:
            redirect: redirect to question page.
        """
        title = request.POST.get('form-input-text-new-question')
        question = Question.objects.create(
            user=request.user,
            title=title
        )
        return HttpResponseRedirect(f'/question/{question.id}/')

class LikeView(View):
    """Handles liking and unliking answers.

    This view manages the process of liking and unliking answers, handling POST requests.
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