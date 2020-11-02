from django.contrib.auth import get_user_model
from django.test import TestCase

from profiles.models import Profile, SocialLink


class ProfilesModelTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            first_name='Bruce', last_name='Wayne',
            email='batman@batman.com', password='imbatman'
        )

    def test_create_profile(self):
        profile = Profile.objects.create(
            occupation='Software Developer',
            contact_email='bruce@wayne.com',
            phone='+5516991230099',
            city='Gothan',
            country='DC Comics',
            user=self.user
        )
        self.assertEqual(profile.occupation, 'Software Developer')
        self.assertEqual(profile.contact_email, 'bruce@wayne.com')
        self.assertEqual(profile.phone, '+5516991230099')
        self.assertEqual(profile.city, 'Gothan')
        self.assertEqual(profile.country, 'DC Comics')
        self.assertEqual(profile.user.first_name, 'Bruce')
        self.assertEqual(str(profile), 'Bruce Wayne')

    def test_create_profile_social_link(self):
        social_link = SocialLink.objects.create(
            github='https://github.com/batman',
            linkedin='https://www.linkedin.com/in/bruce/',
            twitter='https://twitter.com/bruce',
            website='https://wayneenterprises.we/',
        )
        profile = Profile.objects.create(
            occupation='Back-end Developer',
            contact_email='bruce@wayneenterprises.we',
            phone='+5516998760099',
            city='Metropolis',
            country='DC Comics',
            user=self.user,
            social_link=social_link
        )
        self.assertEqual(profile.occupation, 'Back-end Developer')
        self.assertEqual(profile.city, 'Metropolis')
        self.assertEqual(profile.country, 'DC Comics')
        self.assertEqual(profile.user.first_name, 'Bruce')
        self.assertEqual(profile.social_link.github, 'https://github.com/batman')
        self.assertEqual(profile.social_link.linkedin, 'https://www.linkedin.com/in/bruce/')
        self.assertEqual(profile.social_link.twitter, 'https://twitter.com/bruce')
        self.assertEqual(profile.social_link.website, 'https://wayneenterprises.we/')
