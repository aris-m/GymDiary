from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import SignUpForm, WorkoutSessionForm, WorkoutForm, GoalForm
from .models import WorkoutSession, Workout, Goal

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
    workouts = workout_session.workouts.all()
    goals = workout_session.goals.all()
    return render(request, "user_session.html", {"workout_session": workout_session, 'workouts': workouts, 'goals':goals})

@login_required(login_url='login')
def delete_user_session(request, pk):
    workout_session = WorkoutSession.objects.get(id=pk, user=request.user)
    workout_session.delete()
    messages.success(request, "Workout Session Deleted Successfully!")
    return redirect('tracker')

@login_required(login_url='login')
def update_user_session(request, pk):
    workout_session = WorkoutSession.objects.get(id=pk, user=request.user)
    print(workout_session.date)
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST, instance=workout_session)
        if form.is_valid():
            form.save()
            messages.success(request, "Workout Session has been updated!")
            return redirect('tracker')
    else:
        form = WorkoutSessionForm(instance=workout_session) 
    return render(request, "update_session.html", {"form": form, "workout_session": workout_session})

"""
Add/Delete/Update workouts to a workout session
"""

@login_required(login_url='login')
def add_workout(request, session_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            name = form.cleaned_data['name']
            type = form.cleaned_data['type']
            muscle_groups = form.cleaned_data['muscle_groups']
            workout = Workout.objects.create(workout_session=workout_session, name=name,type=type,muscle_groups=muscle_groups)
            workout_session.workouts.add(workout)
            workout.save()
            messages.success(request, "You have added a workout", extra_tags="success")
            
            return HttpResponseRedirect(reverse('session', args=[session_id]) + '?tab=workouts')
        else:
            messages.error(request, "workout failed to be added", extra_tags="error")
            return redirect('add-workout', session_id=session_id)
    form = WorkoutForm()
    return render(request, 'add_workout.html', {'form':form, "workout_session": workout_session})

@login_required(login_url='login')
def delete_workout(request, session_id, workout_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    workout = Workout.objects.get(id=workout_id, workout_session=workout_session)
    workout.delete()
    workouts = workout_session.workouts.all()
    messages.success(request, "Workout Deleted Successfully!")
    return render(request, 'partials/workout_list.html', {"workout_session": workout_session, "workouts":workouts})

@login_required(login_url='login')
def update_workout(request, session_id, workout_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    workout = Workout.objects.get(id=workout_id, workout_session=workout_session)
    
    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, "Workout Updated Successfully!")
            return redirect('session', pk=session_id)
    else:
        form = WorkoutForm(instance=workout) 
    return render(request, "update_workout.html", {"form": form, "workout_session": workout_session, "workout": workout})

"""
add goals to a workout session
"""
@login_required(login_url='login')
def add_goal(request, session_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            description = form.cleaned_data['description']
            accomplished = form.cleaned_data['accomplished']
            goal = Goal.objects.create(workout_session = workout_session, description=description, accomplished=accomplished)
            workout_session.goals.add(goal)
            goal.save()
            messages.success(request, "You have added a goal", extra_tags="success")
            
            goals = workout_session.goals.all()
            return render(request, 'user_session.html', {'workout_session': workout_session, 'goals': goals})
        else:
            messages.error(request, "goal failed to be added", extra_tags="error")
            return redirect('add-goal', session_id=session_id)
    form = GoalForm()
    return render(request, 'add_goal.html', {'form':form, "workout_session": workout_session})

@login_required(login_url='login')
def delete_goal(request, session_id, goal_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    goal = Goal.objects.get(id=goal_id, workout_session=workout_session)
    goal.delete()
    
    goals = workout_session.goals.all()
    messages.success(request, "Goal Deleted Successfully!")
    return render(request, 'partials/goal_list.html', {"workout_session": workout_session, "goals":goals})