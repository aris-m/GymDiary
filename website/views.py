from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import constants
from .forms import SignUpForm

def index(request):
    return render(request, "index.html", {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.", extra_tags="success")
            return redirect("index")
        else:
            messages.error(request, "There was an error while trying to log in, please try again", extra_tags="error")
            return redirect("login")
    
    return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("index")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!", extra_tags="success")
            return redirect('index')
        else:
            messages.error(request, "Registration failed, please try again", extra_tags="error")
            return redirect('register')
    form = SignUpForm()
    return render(request, 'register.html', {'form':form})

def tracker(request):
    pass
	