from django.core.exceptions import ValidationError
from django.test import TestCase

from resume.profiles.models import Profile, SocialLink
from resume.profiles.tests.fixture import ProfileFactory, SocialLinkFactory
from resume.users.tests.fixture import UserFactory


class ProfilesModelTestCase(TestCase):
    def setUp(self) -> None:
        """
        Initial setup to create a user and run the tests.
        """
        self.user = UserFactory.create()

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
            user=self.user,
        )
        self.assertEqual(profile.occupation, 'Software Developer')
        self.assertEqual(profile.contact_email, 'bruce@wayne.com')
        self.assertEqual(profile.phone, '+5516991230099')
        self.assertEqual(profile.city, 'Gothan')
        self.assertEqual(profile.country, 'DC Comics')
        self.assertEqual(profile.user.first_name, self.user.first_name)
        self.assertEqual(str(profile), self.user.get_full_name)
        self.assertEqual(profile.get_location, 'Gothan, DC Comics')

    def test_create_profile_with_about(self) -> None:
        """
        Validate that a profile is being created correctly with 'about' field.
        """
        about = """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been
        the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and
        scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into
        electronic typesetting, remaining essentially unchanged."""

        profile = Profile.objects.create(
            occupation='Software Developer',
            contact_email='bruce@wayne.com',
            about=about,
            phone='+5516991230099',
            city='Gothan',
            country='DC Comics',
            user=self.user,
        )
        self.assertEqual(profile.about, about)

    def test_create_profile_with_more_characters_than_the_limit(self) -> None:
        """
        Validate that a profile is not being created with the 'about' field longer than 550 characters.
        """
        about_with_550_char = 'a' * 550
        profile = ProfileFactory.create(about=about_with_550_char)
        self.assertEqual(profile.about, about_with_550_char)
        with self.assertRaises(
            ValidationError, msg=['Certifique-se de que o valor tenha no máximo 550 caracteres (ele possui 551).']
        ):
            ProfileFactory.create(about=about_with_550_char + 'a').full_clean()


class SocialLinkModelTestCase(TestCase):
    def setUp(self) -> None:
        """
        Initial setup to create a profile and run the tests.
        """
        self.profile = ProfileFactory.create()

    def test_create_social_link(self):
        """
        Validate the creation of a social link.
        """
        data = dict(name='github', link='https://github.com/batman', profile=self.profile)
        social_link = SocialLink.objects.create(**data)
        self.assertEqual(data.get('name'), social_link.name)
        self.assertEqual(data.get('link'), social_link.link)
        self.assertTrue(social_link.is_active)

    def test_social_link_property(self):
        """
        Validate the correct return of social link property.
        """
        social_link = SocialLinkFactory.create(name='website', link='https://wayneenterprises.we/')
        self.assertEqual('', social_link.get_username)
        self.assertEqual('website', str(social_link))

        social_link = SocialLinkFactory.create(name='github', link='https://github.com/batman')
        self.assertEqual('batman', social_link.get_username)
        self.assertEqual('github', str(social_link))

        social_link = SocialLinkFactory.create(name='linkedin', link='https://www.linkedin.com/in/bruce-wayne/')
        self.assertEqual('bruce-wayne', social_link.get_username)
        self.assertEqual('linkedin', str(social_link))

        social_link = SocialLinkFactory.create(name='twitter', link='https://twitter.com/brucew/')
        self.assertEqual('brucew', social_link.get_username)
        self.assertEqual('twitter', str(social_link))

        social_link = SocialLinkFactory.create(name='website', link='https://www.youtube.com/c/EbhDRTEI54E')
        self.assertEqual('', social_link.get_username)
        self.assertEqual('website', str(social_link))
