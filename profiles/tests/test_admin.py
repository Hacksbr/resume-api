from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

from profiles.admin import ProfileAdmin, SocialLinkAdmin
from profiles.models import Profile, SocialLink
from profiles.tests.fixture import ProfileFactory, SocialLinkFactory


class MockUser:

    def has_perm(self, perm):
        return True


class MockProfile:

    def __init__(self):
        self.user = None


class MockSocialLink:

    def __init__(self):
        self.profile = MockProfile()


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockUser()


class ProfileAdminTest(TestCase):

    def setUp(self):
        self.profile = ProfileFactory.create()
        self.admin = ProfileAdmin(model=Profile, admin_site=AdminSite())

    def test_delete_model(self):
        self.assertEqual(self.profile.user.get_full_name, self.admin.user__name(obj=self.profile))
        self.assertEqual('None', self.admin.user__name(obj=MockProfile()))
        self.assertEqual(self.profile.get_location, self.admin.profile__location(obj=self.profile))

        self.assertTrue(request.user.has_perm(perm=None))
        self.admin.delete_model(request, self.profile)
        self.assertFalse(Profile.objects.filter(pk=self.profile.id).exists())


class SocialLinkAdminTest(TestCase):

    def setUp(self):
        self.social_link = SocialLinkFactory.create()
        self.admin = SocialLinkAdmin(model=SocialLink, admin_site=AdminSite())

    def test_delete_model(self):
        self.assertEqual(
            self.social_link.profile.user.get_full_name, self.admin.profile__user__name(obj=self.social_link)
        )
        self.assertEqual('None', self.admin.profile__user__name(obj=MockSocialLink()))

        self.assertTrue(request.user.has_perm(perm=None))
        self.admin.delete_model(request, self.social_link)
        self.assertFalse(SocialLink.objects.filter(pk=self.social_link.id).exists())
