from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from profiles.tests.fixture import ProfileFactory, SocialLinkFactory
from users.tests.fixture import UserFactory

User = get_user_model()

USER_DATA = dict(
    first_name='Bruce',
    last_name='Wayne',
    email='batman@batman.com',
    password='imbatman'
)

SOCIAL_LINK_DATA = [
    dict(name='github', link='https://github.com/batman'),
    dict(name='linkedin', link='https://www.linkedin.com/in/batman'),
    dict(name='twitter', link='https://twitter.com/batman'),
    dict(name='website', link='https://batman.bat/')
]


class ProfileViewSetTests(APITestCase):

    def setUp(self) -> None:
        """
        Initial setup to run the tests.
        """
        self.user = UserFactory.create()

        self.admin_user = UserFactory.create()
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        self.client = APIClient()

        self.data = {
            'user': USER_DATA,
            'occupation': 'Back-end Developer',
            'contact_email': 'bruce@wayneenterprises.we',
            'phone': '+5516998760099',
            'city': 'Metropolis',
            'country': 'DC Comics',
            'social_links': SOCIAL_LINK_DATA,
        }

    def test_perform_create(self) -> None:
        """
        Validate the creation of a complete profile with social link.
        """
        response = self.client.post(reverse('profile-list'), data=self.data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user_data = self.data.get('user', {})
        self.assertEqual(f'{user_data.get("first_name")} {user_data.get("last_name")}', response.data.get('name'))
        self.assertEqual(self.data.get('occupation'), response.data.get('occupation'))
        self.assertEqual(self.data.get('contact_email'), response.data.get('contact_email'))
        self.assertEqual(f'{self.data.get("city")}, {self.data.get("country")}', response.data.get('location'))
        self.assertEqual(self.data.get('phone'), response.data.get('phone'))
        self.assertEqual(len(self.data.get('social_links')), len(response.data.get('social_links')))

    def test_list(self) -> None:
        """
        Validate the listing of created profiles.
        """
        ProfileFactory.create_batch(5)

        self.client.logout()
        response = self.client.get(reverse('profile-list'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('profile-list'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(self.admin_user)
        response = self.client.get(reverse('profile-list'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(5, len(response.data))

    def test_retrieve(self) -> None:
        """
        Validate the return of a specific profile through its identifier.
        """
        profile = ProfileFactory.create()

        response = self.client.get(reverse('profile-detail', args=[profile.uuid]), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(str(profile.uuid), response.data.get('uuid'))
        self.assertEqual(profile.user.get_full_name, response.data.get('name'))
        self.assertEqual(profile.occupation, response.data.get('occupation'))
        self.assertEqual(profile.contact_email, response.data.get('contact_email'))
        self.assertEqual(profile.get_location, response.data.get('location'))
        self.assertEqual(profile.phone, response.data.get('phone'))

    def test_update(self) -> None:
        """
        Validate partial data update of an authenticated profile.
        """
        user = UserFactory.create()
        profile = ProfileFactory.create(user=user)
        social_link1 = SocialLinkFactory.create(profile=profile)
        social_link2 = SocialLinkFactory.create(profile=profile)

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
            'social_links': [
                {
                    'id': social_link1.id,
                    'name': social_link1.name,
                    'link': 'https://github.com/batman',
                    'is_active': True,
                },
                {
                    'id': social_link2.id,
                    'name': social_link2.name,
                    'link': 'https://www.linkedin.com/in/batman',
                    'is_active': True,
                }
            ]
        }

        self.assertNotEqual(data.get('occupation'), profile.occupation)
        self.assertNotEqual(data.get('contact_email'), profile.contact_email)

        self.client.force_authenticate(self.user)

        response = self.client.put(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(user)
        response = self.client.put(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data['occupation'] = 'Developer'

        self.client.force_authenticate(self.admin_user)
        response = self.client.put(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data.get('occupation'), response.data.get('occupation'))

    def test_partial_update(self) -> None:
        """
        Validate the partial update of a profile's data.
        """
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
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_authenticate(user)
        response = self.client.patch(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Attribute \'user\' is missing.', response.data.get('error'))

        self.client.force_authenticate(self.admin_user)
        response = self.client.patch(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Attribute \'user\' is missing.', response.data.get('error'))

        data['user'] = USER_DATA,

        response = self.client.patch(reverse('profile-detail', args=[profile.uuid]), data=data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Attribute \'social_link\' is missing.', response.data.get('error'))

    def test_destroy(self) -> None:
        """
        Validate the deletion of data from an authenticated profile.
        """
        profile = ProfileFactory.create()

        user_id = profile.user_id

        self.assertTrue(User.objects.filter(id=user_id).exists())

        self.client.force_authenticate(self.admin_user)
        response = self.client.get(reverse('profile-detail', args=[profile.uuid]), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(len(response.data.get('uuid')), profile.uuid)

        self.client.logout()
        response = self.client.delete(reverse('profile-detail', args=[profile.uuid]), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(profile.user)
        response = self.client.delete(reverse('profile-detail', args=[profile.uuid]), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertFalse(User.objects.filter(id=user_id).exists())

        self.client.force_authenticate(self.admin_user)
        response = self.client.get(reverse('profile-detail', args=[profile.uuid]), format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
