from django.db import models
from BaseID.models import BaseIdModel
from accounts.models import User

# Create your models here.

class Question(BaseIdModel):
    """Represents a question in the Quora-like platform.

    This model stores information about a question, including its author, title.

    Args:
        BaseIdModel (class): custom made abstract model for avoid repetitiveness.

    Returns:
        String: question title.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_questions')
    title = models.CharField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        return str(self.title)
    
class Answers(BaseIdModel):
    """Represents an answer to a question.

    This model stores information about an answer, including its author,
    the question it belongs to, the answer text, and likes.

    Args:
        BaseIdModel (class): custom made abstract model for avoid repetitiveness.

    Returns:
        String: answer.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked_answers')
    answer = models.TextField(max_length=500, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.answer)
    
    @property
    def likes_count(self):
        """Counts the total number of likes for an answer

        Returns:
            int: The total number of likes.
        """
        return self.liked.all().count()
    
class Likes(BaseIdModel):
    LIKE_CHOICES =(
        ('Like', 'Like'),
        ('Unlike', 'Unlike')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='answer_likes')
    value = models.CharField(choices=LIKE_CHOICES, max_length=10, default='Like')
    objects = models.Manager()

    def __str__(self):
        return str(self.answer)
