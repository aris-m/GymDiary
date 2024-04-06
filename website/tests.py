from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        self.index_url = reverse('index')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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