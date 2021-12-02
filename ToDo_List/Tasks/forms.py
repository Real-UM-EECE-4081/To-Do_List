from django import forms
from django.forms import TextInput, NullBooleanSelect, Textarea, SelectDateWidget
from . import models


class DateInput(forms.DateInput):
    input_type='date'

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = [
            'name',
            'date',
            'recurring',
            'notes',
            'complete'
            ]
        labels = {
            "name": "Task Name",
            "date": "Task Date",
            "recurring": "Recurring Weekly",
        }
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'label': 'Task Name'
            }),
            'date': DateInput(),
            'notes': Textarea(attrs={
                'class': "form-control",
                'required': False,
                'style': 'max-width: 300px;',
                'label': 'Notes'
            })
        }