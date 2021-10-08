import re

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTokenTests(APITestCase):

    def setUp(self):
        self.data = {'email': 'bruce@user.com', 'password': 'foo'}
        self.user = User.objects.create_user(email=self.data.get('email'), password=self.data.get('password'))

        self.regex = r'^[a-zA-Z0-9-_=]+\.[a-zA-Z0-9-_=]+\.?[a-zA-Z0-9-_.+/=]*'

    def test_token_login(self):
        # post to get token
        response = self.client.post(reverse('token_obtain_pair'), data=self.data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(bool(re.search(self.regex, response.data.get('access'))))
        self.assertTrue(bool(re.search(self.regex, response.data.get('refresh'))))

    def test_token_refresh(self):
        # post to get token
        response = self.client.post(reverse('token_obtain_pair'), data=self.data, format='json')
        data = {'refresh': response.data.get('refresh')}

        # post to get refresh token
        response = self.client.post(reverse('token_refresh'), data=data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(bool(re.search(self.regex, response.data.get('access'))))
