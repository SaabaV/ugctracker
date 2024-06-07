from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_profile.models import Profile
from django.core.exceptions import PermissionDenied
from .forms import RegistrationForm
from .token import create_access_token, verify_token


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.profile_url = reverse('user_profile')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = create_access_token(data={"user_id": self.user.id})

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        print("Running test_login_view_post_valid")
        response = self.client.post(self.login_url, {'login': 'testuser', 'password': 'testpassword123'})
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {'login': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login credentials')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_register_view_post_valid(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_register_view_post_invalid(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)


class RegisterFormTestCase(TestCase):
    def test_register_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])


class TokenTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.token = create_access_token(data={"user_id": self.user.id})

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()

    def test_create_access_token(self):
        self.assertIsNotNone(self.token)

    def test_verify_token(self):
        decoded_data = verify_token(self.token, credentials_exception=PermissionDenied)
        self.assertEqual(decoded_data['user_id'], self.user.id)


