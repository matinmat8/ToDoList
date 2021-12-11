from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

PRIORITY_CHOICES = (
    ('WithOUt', 'without'),
    ('First', 'first'),
    ('Second', 'second'),
    ('Third', 'third'),
)


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    title = models.CharField(max_length=75)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ToDoList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('todolist:get_children', kwargs={'pk': self.pk})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    for_work = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, blank=True)
