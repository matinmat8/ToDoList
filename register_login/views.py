from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegister


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
            return redirect('register_login:index')

    else:

        # if request method is get
        # create form by with get request
        form = UserRegister()

    return render(request, 'register_login/register.html', {'form': form})
