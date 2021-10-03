from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from profiles.tests.fixture import ProfileFactory

User = get_user_model()


class ProfileViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve(self):
        profile = ProfileFactory.create()

        response = self.client.get(reverse('profile-detail', args=[profile.uuid]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(str(profile.uuid), response.data.get('uuid'))
        self.assertEqual(profile.user.get_full_name, response.data.get('name'))
        self.assertEqual(profile.occupation, response.data.get('occupation'))
        self.assertEqual(profile.contact_email, response.data.get('contact_email'))
        self.assertEqual(profile.get_location, response.data.get('location'))
        self.assertEqual(profile.phone, response.data.get('phone'))
        self.assertEqual(profile.social_link.github, response.data.get('social_link', {}).get('github'))
        self.assertEqual(profile.social_link.linkedin, response.data.get('social_link', {}).get('linkedin'))
        self.assertEqual(profile.social_link.twitter, response.data.get('social_link', {}).get('twitter'))
        self.assertEqual(profile.social_link.website, response.data.get('social_link', {}).get('website'))
