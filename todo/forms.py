from django.forms import ModelForm
from .models import TodoModel

class Todoform(ModelForm):
    class Meta:
        model = TodoModel
        fields = ['Title','Description','Important']