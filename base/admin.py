from django.contrib import admin
from .models import Question, Answers, Likes

# Register your models here.

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    """Register Question model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'id', 'user','title'
    ]

@admin.register(Answers)
class AnswersModelAdmin(admin.ModelAdmin):
    """Register Answers model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'id', 'user', 'question','answer'
    ]

@admin.register(Likes)
class LikesModelAdmin(admin.ModelAdmin):
    """Register Likes model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'id', 'answer', 'value'
    ]