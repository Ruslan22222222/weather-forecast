from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from weather.models import SearchHistory
import json


class WeatherAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()

        self.search_history = SearchHistory.objects.create(
            user=self.user,
            city='Москва',
            count=1
        )

    def test_login_page(self):
        """Тест страницы входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather-config/auth/login.html')

    def test_login_success(self):
        """Тест успешного входа"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_login_failure(self):
        """Тест неудачного входа"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather-config/auth/login.html')

    def test_logout(self):
        """Тест выхода из системы"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_weather_search_authenticated(self):
        """Тест поиска погоды авторизованным пользователем"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('weather:search'), {
            'city': 'Москва'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('temperature', response.context)
        self.assertIn('weather_description', response.context)

    def test_weather_search_unauthenticated(self):
        """Тест поиска погоды неавторизованным пользователем"""
        response = self.client.post(reverse('weather:search'), {
            'city': 'Москва'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Пожалуйста, войдите в систему', response.content.decode())

    def test_history_view_authenticated(self):
        """Тест просмотра истории авторизованным пользователем"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('weather:history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather-config/partials/history_table.html')
        self.assertIn(self.search_history, response.context['history'])

    def test_history_view_unauthenticated(self):
        """Тест просмотра истории неавторизованным пользователем"""
        response = self.client.get(reverse('weather:history'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/history/')

    def test_history_api_authenticated(self):
        """Тест API истории авторизованным пользователем"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('weather:history_api'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['city'], 'Москва')
        self.assertEqual(data[0]['count'], 1)

    def test_history_api_unauthenticated(self):
        """Тест API истории неавторизованным пользователем"""
        response = self.client.get(reverse('weather:history_api'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/api/history/')

    def test_autocomplete_city(self):
        """Тест автодополнения городов"""
        response = self.client.get(reverse('weather:autocomplete'), {'city': 'Моск'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Москва', response.content.decode())

    def test_search_history_increment(self):
        """Тест увеличения счетчика поиска"""
        self.client.login(username='testuser', password='testpass123')
        initial_count = self.search_history.count

        # Делаем поиск того же города
        self.client.post(reverse('weather:search'), {'city': 'Москва'})

        # Проверяем, что счетчик увеличился
        updated_history = SearchHistory.objects.get(user=self.user, city='Москва')
        self.assertEqual(updated_history.count, initial_count + 1)

    def test_search_history_new_city(self):
        """Тест добавления нового города в историю"""
        self.client.login(username='testuser', password='testpass123')

        # Делаем поиск нового города
        self.client.post(reverse('weather:search'), {'city': 'Санкт-Петербург'})

        # Проверяем, что новый город добавлен в историю
        new_history = SearchHistory.objects.filter(user=self.user, city='Санкт-Петербург').first()
        self.assertIsNotNone(new_history)
        self.assertEqual(new_history.count, 1)

    def test_search_history_user_isolation(self):
        """Тест изоляции истории поиска между пользователями"""
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )

        # Логинимся как второй пользователь
        self.client.login(username='testuser2', password='testpass123')

        # Делаем поиск
        self.client.post(reverse('weather:search'), {'city': 'Москва'})

        # Проверяем, что у второго пользователя своя история
        user2_history = SearchHistory.objects.filter(user=user2, city='Москва').first()
        self.assertIsNotNone(user2_history)
        self.assertEqual(user2_history.count, 1)

        # Проверяем, что история первого пользователя не изменилась
        user1_history = SearchHistory.objects.get(user=self.user, city='Москва')
        self.assertEqual(user1_history.count, 1)
