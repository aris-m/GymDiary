from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class tests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')