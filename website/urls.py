from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'), 
    path('tracker/', views.tracker, name='tracker'),
    path('workout-sessions/', views.workout_sessions, name='workout-sessions'),
    path('create-workout-session/', views.create_workout_session, name='create-workout-session'),
    path('session/<int:pk>', views.user_session, name='session'),
    path('delete-session/<int:pk>', views.delete_user_session, name='delete-session'),
    path('update-session/<int:pk>', views.update_user_session, name='update-session'),
    path('sort-workout-sessions-early-furthest/', views.sort_workout_sessions_early_furthest, name='sort-workout-sessions-early-furthest'),
    path('sort-workout-sessions-furthest-early/', views.sort_workout_sessions_furthest_early, name='sort-workout-sessions-furthest-early'),
    path('add-workout/<int:session_id>', views.add_workout, name='add-workout'),
    path('delete-workout/<int:session_id>/<int:workout_id>/', views.delete_workout, name='delete-workout'),
    path('update-workout/<int:session_id>/<int:workout_id>/', views.update_workout, name='update-workout'),
    path('add-goal/<int:session_id>', views.add_goal, name='add-goal'),
    path('accomplish/<int:session_id>/<int:goal_id>/', views.accomplish, name='accomplish'),
    path('delete-goal/<int:session_id>/<int:goal_id>/', views.delete_goal, name='delete-goal'),
    path('progress/', views.progress, name='progress'),
    path('health-metric/', views.health_metric, name='health-metric'),
    path('add-health-metric/', views.add_health_metric, name='add-health-metric'),
    path('delete-health-metric/<int:metric_id>', views.delete_health_metric, name='delete-health-metric'),
    path('update-health-metric/<int:metric_id>', views.update_health_metric, name='update-health-metric'),
]