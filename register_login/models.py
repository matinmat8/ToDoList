from django.db import models
from django.contrib.auth.models import User

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.signals import user_logged_in


class AccountEmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acceptance = models.BooleanField(default=False)


# Creating an acceptance object in different way of view logic, with signals, but I'd rather the view logic because
# it works just when it calls! but in signals it will always be calling, and it will be a useless process

# @receiver(user_logged_in)
# def callback(user, **kwargs):
#     user = user
#     try:
#         AccountEmailConfirmation.objects.get(user=user)
#         pass
#     except:
#         AccountEmailConfirmation.objects.create(
#             user=user,
#             acceptance=False
#         )