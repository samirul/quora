from django import forms
from .models import Question, Answers

class AskQuestionForm(forms.ModelForm):
    """Form for asking a new question.

    Uses a ModelForm based on the Question model with a customized title field widget.

    Args:
        forms (class): Django forms.
    """
    class Meta:
        """Meta class for AskQuestionForm.

        Specifies the model, fields, and widgets for the form.
        """
        model = Question
        fields = ['title']
        widgets = {'title' : forms.TextInput(attrs={'class' : 'form-control',
                  'style': 'width: 100%; height: 50px;',
                  'placeholder': 'Write your question'})}
        
class WriteCommentForm(forms.ModelForm):
    """Form for writing a new answer.

    Uses a ModelForm based on the Answers model with a customized answer field widget.

    Args:
        forms (class): Django forms.
    """
    class Meta:
        """Meta class for WriteCommentForm.

        Specifies the model, fields, and widgets for the form.
        """
        model = Answers
        fields = ['answer']
        widgets = {'title' : forms.TextInput(attrs={'class' : 'form-control',
                  'style': 'width: 100%; height: 50px;'})}
