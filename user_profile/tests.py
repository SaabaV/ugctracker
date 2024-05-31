from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import AvatarForm


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio', date_of_birth='1990-01-01')

    def test_user_profile_view(self):
        client = Client()
        client.login(username='test_user', password='12345')
        response = client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test bio')

    def test_upload_avatar_view(self):
        client = Client()
        client.login(username='test_user', password='12345')
        response = client.post(reverse('upload_avatar_view'), {'avatar': 'test_avatar.png'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_avatar_form_valid(self):
        form = AvatarForm(data={'avatar': 'test_avatar.png'})
        self.assertTrue(form.is_valid())

    def test_avatar_form_invalid(self):
        form = AvatarForm(data={})
        self.assertFalse(form.is_valid())
