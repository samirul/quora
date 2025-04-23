from django import forms
from .models import Question

class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']
        widgets = {'title' : forms.TextInput(attrs={'class' : 'form-control',
                  'style': 'width: 100%; height: 50px;',
                  'placeholder': 'Write your question'})}