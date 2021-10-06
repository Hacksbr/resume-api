from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from profiles.tests.fixture import ProfileFactory
from users.tests.fixture import UserFactory

User = get_user_model()

USER_DATA = dict(
    first_name='Bruce',
    last_name='Wayne',
    email='batman@batman.com',
    password='imbatman'
)

SOCIAL_LINK_DATA = dict(
    github='https://github.com/batman',
    linkedin='https://www.linkedin.com/in/bruce',
    twitter='https://twitter.com/bruce',
    website='https://wayneenterprises.we/',
)


class ProfileViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory.create()

        self.admin_user = UserFactory.create()
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True

        self.client = APIClient()

        self.data = {
            'user': USER_DATA,
            'occupation': 'Back-end Developer',
            'contact_email': 'bruce@wayneenterprises.we',
            'phone': '+5516998760099',
            'city': 'Metropolis',
            'country': 'DC Comics',
            'social_link': SOCIAL_LINK_DATA,
        }

    def test_perform_create(self):
        response = self.client.post(reverse('profile-list'), data=self.data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user_data = self.data.get('user', {})
        social_link_data = self.data.get('social_link', {})
        social_link = response.data.get('social_link', {})

        self.assertEqual(f'{user_data.get("first_name")} {user_data.get("last_name")}', response.data.get('name'))
        self.assertEqual(self.data.get('occupation'), response.data.get('occupation'))
        self.assertEqual(self.data.get('contact_email'), response.data.get('contact_email'))
        self.assertEqual(f'{self.data.get("city")}, {self.data.get("country")}', response.data.get('location'))
        self.assertEqual(self.data.get('phone'), response.data.get('phone'))
        self.assertEqual(social_link_data.get('github'), social_link.get('github'))
        self.assertEqual(social_link_data.get('linkedin'), social_link.get('linkedin'))
        self.assertEqual(social_link_data.get('twitter'), social_link.get('twitter'))
        self.assertEqual(social_link_data.get('website'), social_link.get('website'))

    def test_retrieve(self) -> None:
        profile = ProfileFactory.create()

        response = self.client.get(reverse('profile-detail', args=[profile.uuid]), format='json')
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

    def test_update(self):
        user = UserFactory.create()
        profile = ProfileFactory.create(user=user)

        data = {
            'user': {
                'first_name': 'Batman',
                'last_name': 'Wayne',
            },
            'occupation': 'Dark Night',
            'contact_email': 'batman@batman.we',
            'phone': '+5516998760099',
            'city': 'Gotham',
            'country': 'DC Comics',
            'social_link': {
                'github': 'https://github.com/batman',
                'linkedin': 'https://www.linkedin.com/in/batman',
                'twitter': 'https://twitter.com/batman',
                'website': 'https://batman.bat/',
            },
        }

        self.assertNotEqual(data.get('occupation'), profile.occupation)
        self.assertNotEqual(data.get('contact_email'), profile.contact_email)

        self.client.force_authenticate(self.user)

        response = self.client.put(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user)
        response = self.client.put(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['occupation'] = 'Developer'

        self.client.force_authenticate(self.admin_user)
        response = self.client.put(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('occupation'), response.data.get('occupation'))

    def test_partial_update(self):
        user = UserFactory.create()
        profile = ProfileFactory.create(user=user)

        data = {
            'occupation': 'Dark Night',
            'contact_email': 'batman@batman.we',
            'phone': '+5516998760099',
            'city': 'Gotham',
            'country': 'DC Comics',
        }

        self.assertNotEqual(data.get('occupation'), profile.occupation)
        self.assertNotEqual(data.get('contact_email'), profile.contact_email)

        self.client.force_authenticate(self.user)

        response = self.client.patch(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user)
        response = self.client.patch(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(self.admin_user)
        response = self.client.patch(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
