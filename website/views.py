from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import SignUpForm, WorkoutSessionForm, WorkoutForm, GoalForm, HealthMetricForm
from .models import HealthMetric, WorkoutSession, Workout, Goal
import plotly.express as px

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
    return render(request, "tracker.html", {})

@login_required(login_url='login')
def workout_sessions(request):
    workout_sessions = WorkoutSession.objects.filter(user=request.user)
    return render(request, "workout_session.html", {"workout_sessions": workout_sessions})

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
            return redirect('workout_sessions')
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
    workout_sessions = WorkoutSession.objects.filter(user=request.user)
    messages.success(request, "Workout Session Deleted Successfully!")
    return render(request, 'partials/workout_sessions_list.html', {"workout_sessions":workout_sessions})

@login_required(login_url='login')
def update_user_session(request, pk):
    workout_session = WorkoutSession.objects.get(id=pk, user=request.user)
    print(workout_session.date)
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST, instance=workout_session)
        if form.is_valid():
            form.save()
            messages.success(request, "Workout Session has been updated!")
            return redirect('workout_sessions')
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
            return HttpResponseRedirect(reverse('session', args=[session_id]) + '?tab=workouts')
    else:
        form = WorkoutForm(instance=workout) 
    return render(request, "update_workout.html", {"form": form, "workout_session": workout_session, "workout": workout})

"""
add/delete/accomplish goals to a workout session
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
            return HttpResponseRedirect(reverse('session', args=[session_id]) + '?tab=goals')
        else:
            messages.error(request, "goal failed to be added", extra_tags="error")
            return redirect('add-goal', session_id=session_id)
    form = GoalForm()
    return render(request, 'add_goal.html', {'form':form, "workout_session": workout_session})

@login_required(login_url='login')
def accomplish(request, session_id, goal_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    goal = Goal.objects.get(id=goal_id, workout_session=workout_session)
    goal.accomplished = True
    goal.save()
    
    goals = workout_session.goals.all()
    messages.success(request, "Goal Accomplished Successfully!")
    return render(request, 'partials/goal_list.html', {"workout_session": workout_session, "goals":goals})
    
@login_required(login_url='login')
def delete_goal(request, session_id, goal_id):
    workout_session = WorkoutSession.objects.get(id=session_id, user=request.user)
    goal = Goal.objects.get(id=goal_id, workout_session=workout_session)
    goal.delete()
    
    goals = workout_session.goals.all()
    messages.success(request, "Goal Deleted Successfully!")
    return render(request, 'partials/goal_list.html', {"workout_session": workout_session, "goals":goals})

"""
view/add health metrics
"""
@login_required(login_url='login')
def health_metric(request):
    health_metrics = HealthMetric.objects.filter(user=request.user)
    return render(request, 'health_metric.html', {"health_metrics" : health_metrics})

@login_required(login_url='login')
def add_health_metric(request):
    if request.method == "POST":
        form = HealthMetricForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            date = form.cleaned_data['date']
            weight = form.cleaned_data['weight']
            unit = form.cleaned_data['unit']
            calories = form.cleaned_data['calories']
            healthMetric = HealthMetric.objects.create(user=request.user, date=date, weight=weight, unit=unit, calories=calories)
            healthMetric.save()
            messages.success(request, "You have added a health metric", extra_tags="success")
            return redirect('health-metric')
        else:
            messages.error(request, "workout session failed to initialize", extra_tags="error")
            return redirect('add-health-metric')
    form = HealthMetricForm()
    return render(request, 'add_health_metric.html', {'form':form})

@login_required(login_url='login')
def delete_health_metric(request, metric_id):
    health_metric = HealthMetric.objects.get(id=metric_id, user=request.user)
    health_metric.delete()
    health_metrics = HealthMetric.objects.filter(user=request.user)
    messages.success(request, "Health Metric Deleted Successfully!")
    return render(request, 'partials/health_metric_list.html', {"health_metrics":health_metrics})

@login_required(login_url='login')
def update_health_metric(request, metric_id):
    health_metric = HealthMetric.objects.get(id=metric_id, user=request.user)
    
    if request.method == "POST":
        form = HealthMetricForm(request.POST, instance=health_metric)
        if form.is_valid():
            form.save()
            messages.success(request, "Health Metric Updated Successfully!")
            return redirect('health-metric')
    else:
        form = HealthMetricForm(instance=health_metric) 
    return render(request, "update_health_metric.html", {"form": form, "health_metric": health_metric})

"""
View Progress
"""
@login_required(login_url='login')
def progress(request):
    total_user_sessions = WorkoutSession.objects.filter(user=request.user).count()
    total_workouts = Workout.objects.filter(workout_session__user=request.user).count()
    total_goals = Goal.objects.filter(workout_session__user=request.user).count()
    total_goals_accomplished = Goal.objects.filter(workout_session__user=request.user, accomplished=True).count()
    
    average_workouts_per_session = total_workouts / total_user_sessions if total_user_sessions > 0 else 0
    average_goals_accomplished = int(total_goals_accomplished / total_goals * 100) if total_user_sessions > 0 else 0
    
    health_metrics = HealthMetric.objects.filter(user=request.user).order_by('date')
    
    dates = [metric.date for metric in health_metrics]
    bodyweights = [metric.weight for metric in health_metrics]
    calories_intake = [metric.calories for metric in health_metrics]
    
    weight_fig = px.line(
        x=dates,
        y=bodyweights,
        title="Bodyweight Progression",
        labels={"x":"Date", "y":"Bodyweight"},
    )
    
    weight_fig.update_layout(
        title={
            'text': "Bodyweight Progression",
            'x':0.5, 
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                family="Arial, sans-serif",
                size=24,
                color="black"
            )
        }
    )
    
    calorie_fig = px.line(
        x=dates,
        y=calories_intake,
        title="Calories Intake",
        labels={"x":"Date", "y":"Calories"},
    )
    
    calorie_fig.update_layout(
        title={
            'text': "Calories Intake",
            'x':0.5, 
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                family="Arial, sans-serif",
                size=24,
                color="black"
            )
        }
    )
    
    weight_chart = weight_fig.to_html()
    calorie_chart = calorie_fig.to_html()
    
    return render(request, "progress.html", {"total_user_sessions":total_user_sessions, "average_workouts_per_session": average_workouts_per_session, "average_goals_accomplished":average_goals_accomplished, "weight_chart":weight_chart, "calorie_chart":calorie_chart})