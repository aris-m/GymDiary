from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'), 
    path('tracker/', views.tracker, name='tracker'),
    path('create-workout-session/', views.create_workout_session, name='create-workout-session'),
    path('session/<int:pk>', views.user_session, name='session'),
    # path('workouts/<int:session_id>', views.workouts, name='workouts'),
    path('add-workout/<int:session_id>', views.add_workout, name='add-workout'),
]