from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .forms import SignUpForm, WorkoutSessionForm, WorkoutForm
from .models import WorkoutSession


def index(request):
    return render(request, "index.html", {})

"""
Login/Logout/Register for user
"""

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

"""
Workout Tracker (view workout sessions, add workout session, view individual session)
"""
@login_required(login_url='login')
def tracker(request):
    workout_sessions = WorkoutSession.objects.filter(user=request.user)
    return render(request, "tracker.html", {"workout_sessions": workout_sessions})

@login_required(login_url='login')
def create_workout_session(request):
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            date = form.cleaned_data['date']
            duration = form.cleaned_data['duration']
            notes = form.cleaned_data['notes']
            workout_session = WorkoutSession.objects.create(user=request.user, date=date, duration=duration, notes=notes)
            workout_session.user = request.user
            workout_session.save()
            messages.success(request, "You have created a workout session", extra_tags="success")
            return redirect('tracker')
        else:
            messages.error(request, "workout session failed to initialize", extra_tags="error")
            return redirect('create-workout-session')
    form = WorkoutSessionForm()
    return render(request, 'create_session.html', {'form':form})

@login_required(login_url='login')
def user_session(request, pk):
    workout_session = WorkoutSession.objects.get(id=pk, user=request.user)
    return render(request, "user_session.html", {"workout_session": workout_session})

"""
Add workouts to a workout session
"""
@login_required(login_url='login')
def workouts(request, session_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    workouts = workout_session.workouts.all()
    
    return render(request, 'session_workouts.html', {'workout_session': workout_session, 'workouts': workouts})

# @login_required(login_url='login')
# def add_workout(request):
#     if request.method == "POST":
#         form = WorkoutForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
            
#             messages.success(request, "You have created a workout session", extra_tags="success")
#             return redirect('tracker')
#         else:
#             messages.error(request, "workout session failed to initialize", extra_tags="error")
#             return redirect('create-workout-session')
#     form = WorkoutForm()
#     return render(request, 'workout_form.html', {'form':form})

	