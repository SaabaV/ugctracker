from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from user_profile.models import Profile


class UserProfileTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # Создаем профиль для пользователя
        self.profile = Profile.objects.create(user=self.user, bio='Test bio', date_of_birth='2000-01-01')

    def test_user_profile_view(self):
        # Проверяем, что страница профиля пользователя доступна
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)

    def test_upload_avatar_view(self):
        # Проверяем загрузку аватара пользователя
        self.client.force_login(self.user)
        with open('path_to_your_test_image.jpg', 'rb') as img:
            response = self.client.post(reverse('upload_avatar_view'), {'avatar': img})
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешной загрузки

    def test_avatar_form_valid(self):
        # Проверяем форму загрузки аватара с корректными данными
        self.client.force_login(self.user)
        with open('path_to_your_test_image.jpg', 'rb') as img:
            response = self.client.post(reverse('upload_avatar_view'), {'avatar': img})
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешной загрузки

    def test_avatar_form_invalid(self):
        # Проверяем форму загрузки аватара с некорректными данными
        self.client.force_login(self.user)
        response = self.client.post(reverse('upload_avatar_view'), {})  # Пустой POST запрос
        self.assertEqual(response.status_code, 200)  # Проверяем статус код страницы после некорректной загрузки
