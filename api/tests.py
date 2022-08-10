import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from django.contrib.auth import get_user_model

User = get_user_model()

from app.models import Task
from .serializers import CustomAuthTokenSerializer, TaskListSerializer, UserDataSerializer

from datetime import date


class TaskTests(APITestCase):
    list_url = reverse('tasks-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='qwer123',
            email_verify=True
        )
        self.user_not_verified_email = User.objects.create_user(
            username='test',
            email='test1@test.com',
            password='qwer123123',

        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.task = Task.objects.create(name="Task0",
                                        full_text="full text for task",
                                        deadline_date=date.today(),
                                        owner=self.user)
        self.task1 = Task.objects.create(name="Task1",
                                         full_text="full text for task",
                                         deadline_date=date.today(),
                                         status='finished',
                                         owner=self.user
                                         )

        self.task2 = Task.objects.create(name="Task2",
                                         full_text="full text for task",
                                         deadline_date=date.today(),
                                         status='finished',
                                         owner=self.user
                                         )
        self.task3 = Task.objects.create(name="Task3",
                                         full_text="full text for task",
                                         deadline_date=date.today(),
                                         status='finished',
                                         owner=self.user_not_verified_email
                                         )

        print(self.task)
        print(reverse('tasks-list') + '&status=finish')

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_negative(self):
        data = {
            'username': 'test1@test.com',
            'password': 'qwer123123'
        }
        response = self.client.post(reverse('drf-login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Check your email, and verify it!')

    def test_login(self):
        data = {
            # 'username': self.user.email,
            # 'password': self.user.password
            'username': 'test@test.com',
            'password': 'qwer123'
        }
        response = self.client.post(reverse('drf-login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_data_authenticated(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)

    def test_get_user_data_un_authenticated(self):
        self.client.credentials()
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_data_authenticated(self):
        data = {'first_name': 'Changed', 'last_name': 'Changed_second_name'}
        response = self.client.patch(reverse('user-detail', kwargs={'pk': self.user.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["first_name"], 'Changed')
        # self.assertEqual(response.data["last_name"], 'Changed_second_name')
        self.assertEqual(User.objects.get(id=self.user.id).first_name, 'Changed')
        self.assertEqual(User.objects.get(id=self.user.id).last_name, 'Changed_second_name')

    def test_create_tasks_authenticated(self):
        data = {"name": "Task1", "full_text": "full text for task1", "deadline_date": date.today()}
        response = self.client.post(reverse('tasks-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 5)

    def test_create_tasks_un_authenticated(self):
        self.client.credentials()
        data = {"name": "Task1", "full_text": "full text for task1", "deadline_date": date.today()}
        response = self.client.post(reverse('tasks-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_task_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_list_un_authenticated(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_task_detail_authenticated(self):
        response = self.client.get(reverse('tasks-detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_detail_authenticated_on_another_user_task(self):
        response = self.client.get(reverse('tasks-detail', kwargs={'pk': self.task3.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_task_detail_authenticated(self):
        data = {'full_text': 'Changed test'}
        response = self.client.patch(reverse('tasks-detail', kwargs={'pk': self.task.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).full_text, 'Changed test')

    def test_put_task_detail_authenticated(self):
        data = {
            "name": self.task.name,
            "full_text": "Changed full text",
        }
        response = self.client.put(reverse('tasks-detail', kwargs={'pk': self.task.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).full_text, 'Changed full text')

    def test_put_task_detail_un_authenticated(self):
        self.client.credentials()
        data = {
            "name": self.task.name,
            "full_text": "Changed full text",
        }
        response = self.client.put(reverse('tasks-detail', kwargs={'pk': self.task.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dell_task_detail_authenticated(self):
        response = self.client.delete(reverse('tasks-detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_dell_task_detail_un_authenticated(self):
        self.client.credentials()
        response = self.client.delete(reverse('tasks-detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_as_important(self):
        self.assertEqual(self.task1.importance, False)
        response = self.client.post(reverse('tasks-mark-as-important', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task1.id).importance, True)

    def test_set_priority_as_low(self):
        self.assertEqual(self.task.priority, 'medium')
        response = self.client.post(reverse('tasks-set-priority-as-low', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).priority, 'low')

    def test_set_priority_as_high(self):
        self.assertEqual(self.task1.priority, 'medium')
        response = self.client.post(reverse('tasks-set-priority-as-high', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task1.id).priority, 'high')

    def test_set_status_finished(self):
        self.assertEqual(self.task.status, 'todo')
        response = self.client.post(reverse('tasks-set-status-as-finished', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).status, 'finished')

    def test_set_status_blocked(self):
        self.assertEqual(self.task2.status, 'finished')
        response = self.client.post(reverse('tasks-set-status-as-blocked', kwargs={'pk': self.task2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task2.id).status, 'blocked')

    def test_set_status_in_progress(self):
        self.assertEqual(self.task1.status, 'finished')
        response = self.client.post(reverse('tasks-set-status-as-in-progress', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task1.id).status, 'in_progress')

    def test_set_status_todo(self):
        self.task.status = 'finished'
        self.assertEqual(self.task.status, 'finished')
        response = self.client.post(reverse('tasks-set-status-as-todo', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).status, 'todo')

    def test_filter_finished(self):
        response = self.client.get(reverse('tasks-list') + '?status=finished')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_filter_blocked(self):
        response = self.client.get(reverse('tasks-list') + '?status=blocked')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_search(self):
        response = self.client.get(reverse('tasks-list') + '?search=task')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_search1(self):
        response = self.client.get(reverse('tasks-list') + '?search=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_none(self):
        response = self.client.get(reverse('tasks-list') + '?search=89')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
