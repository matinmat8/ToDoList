from django.forms import ModelForm
from django import forms
from .models import ToDoList, PRIORITY_CHOICES, Comment


class AddWorkForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'due_date', 'priority']

    def __init__(self, *args, **kwargs):
        super(AddWorkForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': "form-control form-control-lg",
            'label': 'Title',
            'placeholder': 'Add new work...'
        }),
        self.fields['description'].widget.attrs.update({
            'class': "form-floating form-control",
            'placeholder': 'description'
        }),
        self.fields['priority'].widget.attrs.update({
            'class': 'form-select input-sm'
        }),
        self.fields['due_date'].widget.attrs.update({
            'class': 'form-control input-sm', 'id': 'due_date',
        }),


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


class UpdateWorkForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'due_date', 'priority']

    def __init__(self, *args, **kwargs):
        super(UpdateWorkForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': "form-control form-control-lg",
            'label': 'Title',
            'placeholder': 'Add new work...'
        }),
        self.fields['description'].widget.attrs.update({
            'class': "form-floating form-control",
            'placeholder': 'description'
        }),
        self.fields['priority'].widget.attrs.update({
            'class': 'form-select input-sm'
        }),
        self.fields['due_date'].widget.attrs.update({
            'class': 'form-control input-sm', 'id': 'due_date',
        }),