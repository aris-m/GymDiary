from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import WorkoutSession, Workout, Goal
from datetime import datetime

class tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        self.index_url = reverse('index')
        self.tracker_url = reverse('tracker')
        self.workout_sessions_url = reverse('workout-sessions')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
    
    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
    
    def test_view_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_register_user_valid_input_data(self):
        response = self.client.post(self.register_url, {'username': 'newuser', 'email': 'newuser@gmail.com', 'password1': 'Newpassword#123', 'password2': 'Newpassword#123'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, self.index_url)
    
    def test_register_user_invalid_input_data(self):
        response = self.client.post(self.register_url, {'username': 'newuser', 'email': 'newuser@gmail.com', 'password1': 'Newpassword#123', 'password2': 'Newpassword#345'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, self.register_url)
    
    def test_view_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_tracker_view(self):
        response = self.client.get(self.tracker_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker.html')
        
    def test_view_workout_sessions(self):
        WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        response = self.client.get(self.workout_sessions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workout_session.html')
        self.assertTrue('workout_sessions' in response.context)
        self.assertEqual(len(response.context['workout_sessions']), 1)
    
    def test_view_user_session(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        self.workout = Workout.objects.create(workout_session=self.session, name='Test Workout', type='Strength Training', muscle_groups='chest,arms')
        self.goal = Goal.objects.create(workout_session=self.session, description='Test Goal', accomplished=False)
        self.session.goals.add(self.goal)
        self.session.workouts.add(self.workout)
        
        url = reverse('session', kwargs={'pk': self.session.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_session.html')
        self.assertTrue('workout_session' in response.context)
        self.assertTrue('workouts' in response.context)
        self.assertTrue('goals' in response.context)
        self.assertEqual(response.context['workout_session'], self.session)
        self.assertEqual(len(response.context['goals']), 1)
        self.assertEqual(len(response.context['workouts']), 1)
        
    def test_delete_user_session(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        url = reverse('delete-session', kwargs={'pk': self.session.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/workout_sessions_list.html')
        self.assertEqual(len(response.context['workout_sessions']), 0)
        
    def test_view_update_session(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        url = reverse('update-session', kwargs={'pk': self.session.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_session.html')
        self.assertEqual(response.context['workout_session'], self.session)
        
    def test_update_session(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-05', duration=120, notes='test session')
        url = reverse('update-session', kwargs={'pk': self.session.pk})
        data = {
            'date': datetime.strptime('2024-04-07', '%Y-%m-%d').date(),
            'duration': 60,
            'notes': 'test notes',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.workout_sessions_url)
        updated_session = WorkoutSession.objects.get(pk=self.session.pk)
        self.assertEqual(updated_session.date, datetime.strptime('2024-04-07', '%Y-%m-%d').date())
        self.assertEqual(updated_session.duration, 60)
        self.assertEqual(updated_session.notes, 'test notes')