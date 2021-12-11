from django.forms import ModelForm
from django import forms
from .models import ToDoList, PRIORITY_CHOICES, Comment


class AddWorkForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'due_date', 'priority']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control form-control-lg border-0 add-todo-input bg-transparent rounded w-25 mt-1 mx-3",
                'label': 'Title',
                'placeholder': 'Add new work...'
            }),
            'description': forms.Textarea(attrs={
                'class': "form-floating form-control w-25 mx-3",
                'placeholder': 'description'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select w-25 mx-3',
            }),
            'due_date': forms.DateInput(attrs={'class': 'form-control w-25 mx-3', 'id': 'due_date',
                                               })
        }


class FilterForm(forms.Form):
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    due_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateInput(
        attrs={'class': 'form-control w-25 mx-3',
               'id': 'due_date'}))
    done = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['priority'].widget.attrs.update({
            'class': 'form-select w-25 mx-3',
        }),
        self.fields['done'].widget.attrs.update({
            'class': 'form-check-label mx-3',
        }),


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({
            'class': 'form-control w-25 mx-3 mt-2'
        })
