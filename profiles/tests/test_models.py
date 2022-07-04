from django.contrib.auth import get_user_model
from django.test import TestCase

from profiles.models import Profile, SocialLink

User = get_user_model()

SOCIAL_LINK_DATA = dict(
    github='https://github.com/batman',
    linkedin='https://www.linkedin.com/in/bruce',
    twitter='https://twitter.com/bruce',
    website='https://wayneenterprises.we/',
)


class ProfilesModelTestCase(TestCase):

    def setUp(self) -> None:
        """
        Initial setup to create a user and run the tests.
        """
        self.user = User.objects.create_user(
            first_name='Bruce', last_name='Wayne',
            email='batman@batman.com', password='imbatman'
        )

    def test_create_profile(self) -> None:
        """
        Validate that a profile is being created correctly.
        """
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
        self.assertEqual(profile.get_location, 'Gothan, DC Comics')

    def test_create_profile_social_link(self) -> None:
        """
        Validate if a profile is being created with a social link.
        """
        social_link = SocialLink.objects.create(**SOCIAL_LINK_DATA)
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
        self.assertEqual(profile.social_link.github, SOCIAL_LINK_DATA.get('github'))
        self.assertEqual(profile.social_link.linkedin, SOCIAL_LINK_DATA.get('linkedin'))
        self.assertEqual(profile.social_link.twitter, SOCIAL_LINK_DATA.get('twitter'))
        self.assertEqual(profile.social_link.website, SOCIAL_LINK_DATA.get('website'))


class SocialLinkModelTestCase(TestCase):

    def test_create_social_link(self):
        """
        Validate the creation of a social link.
        """
        social_link = SocialLink.objects.create(**SOCIAL_LINK_DATA)
        self.assertEqual(SOCIAL_LINK_DATA.get('github'), social_link.github)
        self.assertEqual(SOCIAL_LINK_DATA.get('linkedin'), social_link.linkedin)
        self.assertEqual(SOCIAL_LINK_DATA.get('twitter'), social_link.twitter)
        self.assertEqual(SOCIAL_LINK_DATA.get('website'), social_link.website)
        self.assertEqual('batman', social_link.get_github_user)
        self.assertEqual('bruce', social_link.get_linkedin_user)
        self.assertEqual('bruce', social_link.get_twitter_user)

    def test_social_link_attr(self):
        """
        Validate the creation of the attributes of a social link.
        """
        social_link = SocialLink.objects.create(website=SOCIAL_LINK_DATA.get('website'))
        self.assertEqual(SOCIAL_LINK_DATA.get('website'), str(social_link))
        social_link = SocialLink.objects.create(twitter=SOCIAL_LINK_DATA.get('twitter'))
        self.assertEqual('bruce', str(social_link))
        social_link = SocialLink.objects.create(linkedin=SOCIAL_LINK_DATA.get('linkedin'))
        self.assertEqual('bruce', str(social_link))
        social_link = SocialLink.objects.create(github=SOCIAL_LINK_DATA.get('github'))
        self.assertEqual('batman', str(social_link))
