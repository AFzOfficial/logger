from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Log


class LoggerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logger/index.html')

    def test_log_view(self):
        log = Log.objects.create(user=self.user, body='Test Log')
        response = self.client.get(reverse('log', args=[log.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logger/log.html')

    def test_account_profile_view(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logger/profile.html')

    def test_login_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_update_profile(self):
        response = self.client.post(reverse('update_profile'), {
            'username': 'Testing',
            'first_name': 'Test'
        })

        self.user.profile.premium = timezone.now() + timezone.timedelta(1)
        self.user.profile.save()
        
        self.user.refresh_from_db()  

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logger/update_user.html')
        self.assertEqual(self.user.username, 'Testing')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertTrue(self.user.profile.is_premium())
