from django.contrib.auth.models import User
from django.db import models


PRIORITY_CHOICES = (
    ('WithOUt', 'without'),
    ('First', 'first'),
    ('Second', 'second'),
    ('Third', 'third'),
)


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    due_date = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    reminder = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    slug = models.SlugField()

    def __str__(self):
        return self.title