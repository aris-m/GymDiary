from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import HealthMetricForm, WorkoutSessionForm
from .models import HealthMetric, WorkoutSession, Workout, Goal, FriendshipList, FriendshipRequest
from datetime import datetime
from django.contrib.messages import get_messages

class tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        self.index_url = reverse('index')
        self.tracker_url = reverse('tracker')
        self.workout_sessions_url = reverse('workout-sessions')
        self.create_session_url = reverse('create-workout-session')
        self.sort_workout_sessions_early_furthest = reverse('sort-workout-sessions-early-furthest')
        self.sort_workout_sessions_furthest_early = reverse('sort-workout-sessions-furthest-early')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        FriendshipList.objects.create(user=self.user)
        FriendshipList.objects.create(user=self.user2)
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
    
    def test_view_create_workout_session(self):
        response = self.client.get(self.create_session_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_session.html')
        self.assertIsInstance(response.context['form'], WorkoutSessionForm)
    
    def test_create_workout_session(self):
        data = {
            'date': datetime.strptime('2024-04-07', '%Y-%m-%d').date(),
            'duration': 60,
            'notes': 'test session notes',
        }
        response = self.client.post(self.create_session_url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.workout_sessions_url)  

        created_session = WorkoutSession.objects.last()
        self.assertEqual(created_session.user, self.user)
        self.assertEqual(created_session.date, datetime.strptime('2024-04-07', '%Y-%m-%d').date())
        self.assertEqual(created_session.duration, 60)
        self.assertEqual(created_session.notes, 'test session notes')
    
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
    
    def test_sort_workout_sessions_early_furthest(self):
        session1 = WorkoutSession.objects.create(user=self.user, date='2024-04-05', duration=60, notes='test session 1')
        session2 = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session 2')
        session3 = WorkoutSession.objects.create(user=self.user, date='2024-04-06', duration=60, notes='test session 3')

        response = self.client.get(self.sort_workout_sessions_early_furthest)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workout_session.html')
        self.assertTrue('workout_sessions' in response.context)

        sorted_sessions = response.context['workout_sessions']
        self.assertEqual(len(sorted_sessions), 3)
        self.assertEqual(sorted_sessions[0], session1)
        self.assertEqual(sorted_sessions[1], session3)
        self.assertEqual(sorted_sessions[2], session2)
        
    def test_sort_workout_sessions_furthest_early(self):
        session1 = WorkoutSession.objects.create(user=self.user, date='2024-04-05', duration=60, notes='test session 1')
        session2 = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session 2')
        session3 = WorkoutSession.objects.create(user=self.user, date='2024-04-06', duration=60, notes='test session 3')

        response = self.client.get(self.sort_workout_sessions_furthest_early)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workout_session.html')
        self.assertTrue('workout_sessions' in response.context)

        sorted_sessions = response.context['workout_sessions']
        self.assertEqual(len(sorted_sessions), 3)
        self.assertEqual(sorted_sessions[0], session2)
        self.assertEqual(sorted_sessions[1], session3)
        self.assertEqual(sorted_sessions[2], session1)
    
    def test_add_workout(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        url = reverse('add-workout', kwargs={'session_id': self.session.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_workout.html')
        self.assertEqual(response.context['workout_session'], self.session)
        
        data = {
            'name': 'Test Workout',
            'type': 'Strength Training',
            'muscle_groups': 'chest,arms',
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('session', kwargs={'pk': self.session.pk}) + '?tab=workouts')
        self.assertEqual(self.session.workouts.count(), 1)
        added_workout = self.session.workouts.first()
        self.assertEqual(added_workout.name, 'Test Workout')
        self.assertEqual(added_workout.type, 'Strength Training')
        self.assertEqual(added_workout.muscle_groups, "['chest,arms']")
    
    def test_delete_workout(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        self.workout = Workout.objects.create(workout_session=self.session, name='Test Workout', type='Strength Training', muscle_groups='chest,arms')
        url = reverse('delete-workout', kwargs={'session_id': self.session.pk, 'workout_id':self.workout.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/workout_list.html')
        self.assertEqual(len(response.context['workouts']), 0)
    
    def test_update_workout(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        self.workout = Workout.objects.create(workout_session=self.session, name='Test Workout', type='Strength Training', muscle_groups='chest,arms')
        url = reverse('update-workout', kwargs={'session_id': self.session.pk, 'workout_id': self.workout.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_workout.html')
        self.assertEqual(response.context['workout_session'], self.session)
        self.assertEqual(response.context['workout'], self.workout)
       
        updated_data = {
            'name': 'Updated Workout',
            'type': 'Cardio',
            'muscle_groups': 'legs',
        }
        
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('session', kwargs={'pk': self.session.pk}) + '?tab=workouts')
        updated_workout = Workout.objects.get(pk=self.workout.pk)
        self.assertEqual(updated_workout.name, 'Updated Workout')
        self.assertEqual(updated_workout.type, 'Cardio')
        self.assertEqual(updated_workout.muscle_groups, "['legs']")
    
    def test_add_goal(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        url = reverse('add-goal', kwargs={'session_id': self.session.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_goal.html')
        self.assertEqual(response.context['workout_session'], self.session)

        data = {
            'description': 'Test Goal',
            'accomplished': False,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('session', kwargs={'pk': self.session.pk}) + '?tab=goals')
        self.assertEqual(self.session.goals.count(), 1)
        added_goal = self.session.goals.first()
        self.assertEqual(added_goal.description, 'Test Goal')
        self.assertEqual(added_goal.accomplished, False)

    def test_accomplish_goal(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        self.goal = Goal.objects.create(workout_session=self.session, description='Test Goal', accomplished=False)

        url = reverse('accomplish', kwargs={'session_id': self.session.pk, 'goal_id': self.goal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.goal.refresh_from_db()
        self.assertTrue(self.goal.accomplished)

    def test_delete_goal(self):
        self.session = WorkoutSession.objects.create(user=self.user, date='2024-04-07', duration=60, notes='test session')
        self.goal = Goal.objects.create(workout_session=self.session, description='Test Goal', accomplished=False)

        url = reverse('delete-goal', kwargs={'session_id': self.session.pk, 'goal_id': self.goal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.session.goals.count(), 0)

    def test_view_health_metric(self):
        response = self.client.get(reverse('health-metric'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health_metric.html')
        self.assertTrue('health_metrics' in response.context)

    def test_add_health_metric(self):
        response = self.client.get(reverse('add-health-metric'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_health_metric.html')
        self.assertIsInstance(response.context['form'], HealthMetricForm)

        data = {
            'date': datetime.strptime('2024-04-07', '%Y-%m-%d').date(),
            'weight': 70,
            'unit': 'kg',
            'calories': 2000,
        }
        
        response = self.client.post(reverse('add-health-metric'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('health-metric'))
        self.assertTrue(HealthMetric.objects.filter(user=self.user, date=data['date']).exists())

    def test_delete_health_metric(self):
        self.metric = HealthMetric.objects.create(user=self.user, date='2024-04-07', weight=70, unit='kg', calories=2000)
        response = self.client.get(reverse('delete-health-metric', kwargs={'metric_id': self.metric.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/health_metric_list.html')
        self.assertFalse(HealthMetric.objects.filter(id=self.metric.pk).exists())

    def test_update_health_metric(self):
        self.metric = HealthMetric.objects.create(user=self.user, date='2024-04-07', weight=70, unit='kg', calories=2000)
        url = reverse('update-health-metric', kwargs={'metric_id': self.metric.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_health_metric.html')
        self.assertEqual(response.context['health_metric'], self.metric)

        updated_data = {
            'date': datetime.strptime('2024-04-07', '%Y-%m-%d').date(),
            'weight': 75,
            'unit': 'kg',
            'calories': 2200,
        }

        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('health-metric'))
        self.metric.refresh_from_db()
        self.assertEqual(self.metric.date, updated_data['date'])
        self.assertEqual(self.metric.weight, updated_data['weight'])
        self.assertEqual(self.metric.unit, updated_data['unit'])
        self.assertEqual(self.metric.calories, updated_data['calories'])
    
    def test_progress_view(self):
        WorkoutSession.objects.create(user=self.user)
        Workout.objects.create(workout_session=WorkoutSession.objects.first())
        Goal.objects.create(workout_session=WorkoutSession.objects.first())
        HealthMetric.objects.create(user=self.user, weight=70, unit='kg', calories=2000)
        
        response = self.client.get(reverse('progress'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress.html')
        self.assertTrue('total_user_sessions' in response.context)
        self.assertTrue('average_workouts_per_session' in response.context)
        self.assertTrue('average_goals_accomplished' in response.context)
        self.assertTrue('weight_chart' in response.context)
        self.assertTrue('calorie_chart' in response.context)
    
    def test_friend_progress_view(self):
        friend = User.objects.create_user(username='friend', password='testpassword')
        WorkoutSession.objects.create(user=friend)
        Workout.objects.create(workout_session=WorkoutSession.objects.first())
        Goal.objects.create(workout_session=WorkoutSession.objects.first())
        HealthMetric.objects.create(user=friend, weight=150, unit='lbs', calories=1500)

        response = self.client.get(reverse('friend-progress', kwargs={'friend_id': friend.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friend_progress.html')
        self.assertTrue('friend' in response.context)
        self.assertTrue('total_sessions' in response.context)
        self.assertTrue('average_workouts_per_session' in response.context)
        self.assertTrue('average_goals_accomplished' in response.context)
        self.assertTrue('weight_chart' in response.context)
        self.assertTrue('calorie_chart' in response.context)

    def test_friends_list(self):
        response = self.client.get(reverse('community'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community.html')
        self.assertTrue('friendshipList' in response.context)
        self.assertTrue('friend_requests' in response.context)
    
    def test_send_friend_request(self):
        response = self.client.post(reverse('send-friend-request', kwargs={'friend_id':self.user2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/friend-list.html')
        self.assertTrue('friendshipList' in response.context)
        self.assertTrue('friend_requests' in response.context)
        self.assertTrue(FriendshipRequest.objects.filter(sender=self.user, receiver=self.user2).exists())
        
        response = self.client.post(reverse('send-friend-request', kwargs={'friend_id':self.user2.pk}))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue("You have already sent a friend request to this user." in messages)
        
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(reverse('send-friend-request', kwargs={'friend_id':self.user.pk}))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue("This user have already sent you a friend request." in messages)
    
    def test_reject_friend_request(self):
        FriendshipRequest.objects.create(sender=self.user2, receiver=self.user)
        response = self.client.post(reverse('reject-friend-request', kwargs={'request_id': FriendshipRequest.objects.first().pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/friend-list.html')
        self.assertTrue('friendshipList' in response.context)
        self.assertTrue('friend_requests' in response.context)
        self.assertFalse(FriendshipRequest.objects.filter(sender=self.user2, receiver=self.user).exists())
    
    def test_add_friend(self):
        FriendshipRequest.objects.create(sender=self.user2, receiver=self.user)
        response = self.client.post(reverse('add-friend', kwargs={'friend_id': self.user2.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/friend-list.html')
        self.assertTrue('friendshipList' in response.context)
        self.assertTrue('friend_requests' in response.context)
        self.assertTrue(self.user2 in FriendshipList.objects.get(user=self.user).friends.all())
    
    def test_search_friends(self):
        User.objects.create_user(username='user3', password='testpassword3')
        response = self.client.post(reverse('search-friends'), {'search': 'user3'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/search-friends-result.html')
        self.assertTrue('results' in response.context)
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0].username, 'user3')                                                                                      
    
    def test_unfriend(self):
        FriendshipList.objects.get(user=self.user).friends.add(self.user2)
        FriendshipList.objects.get(user=self.user2).friends.add(self.user)
        
        response = self.client.post(reverse('unfriend', kwargs={'friend_id': self.user2.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/friend-list.html')
        self.assertTrue('friendshipList' in response.context)
        self.assertTrue('friend_requests' in response.context)
        self.assertFalse(self.user2 in FriendshipList.objects.get(user=self.user).friends.all())
        self.assertFalse(self.user in FriendshipList.objects.get(user=self.user2).friends.all())