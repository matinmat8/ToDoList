from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail

from .forms import UserRegister, AccountActivationForm
from .models import AccountEmailConfirmation


def register(request):
    if request.method == 'POST':

        # Create form with Post request
        form = UserRegister(request.POST)

        # If everything OK save it
        if form.is_valid():
            # Save Data
            form.save()

            # Get username & password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Create a user with the information we got from the form
            user = authenticate(username=username, password=password)

            # Login the user with login
            login(request, user)
            return redirect('todolist:list')

    else:

        # if request method is get
        # create form by with get request
        form = UserRegister()

    return render(request, 'register_login/register.html', {'form': form})


class EmailConfirmation(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            obj = AccountEmailConfirmation.objects.get(user=user)
        except:
            obj = AccountEmailConfirmation.objects.create(user=user)

        if not obj.acceptance:
            url = 'https://safe-basin-70691.herokuapp.com/register_login/email_confirmation/%s/' % user.pk

            send_mail(subject='Confirmation Email for ToDoList WebSite',
                      message="Dear %s confirm your Email with this link, %s , which that allows us to make sure that "
                              "this email belongs to you and that we can perform Email related operations."
                              % (user.username, url),
                      from_email="todolistmat8@gmail.com", recipient_list=[user.email])

            return render(self.request, 'register_login/email_confirmation.html',
                          {'subject': "We have sent you an email which you can confirm your Email with it."})

        else:
            return render(self.request, 'register_login/email_confirmation.html',
                          {'subject': "Your Email has already been accepted."})


class AccountActivation(View):
    def get(self, *args, **kwargs):
        try:
            obj = AccountEmailConfirmation.objects.get(user=self.request.user)
        except:
            return render(self.request, 'register_login/email_confirmation.html',
                          {'subject': "Please try again with another Email Confirmation"})
        if not obj.acceptance:
            form = AccountActivationForm(self.request.POST or None)
            return render(self.request, 'register_login/getting_email_confirmation_password.html', {'form': form})
        else:
            return render(self.request, 'register_login/email_confirmation.html',
                          {'subject': "Your Email has already been accepted."})

    def post(self, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        password = self.request.POST.get('password')
        password_checking = user.check_password(password)
        # print(password, user.password)
        if password_checking:
            obj = AccountEmailConfirmation.objects.get(user=user)
            obj.acceptance = True
            obj.save()
            return render(self.request, 'register_login/getting_email_confirmation_password.html', {'subject': 'true'})
        else:
            return render(self.request, 'register_login/getting_email_confirmation_password.html', {'subject': 'false'})
