from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

from resume.users.admin import UserAdmin
from resume.users.models import User
from resume.users.tests.fixture import UserFactory


class MockUser:

    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockUser()


class ProfileAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.admin = UserAdmin(model=User, admin_site=AdminSite())

    def test_delete_model(self):
        self.assertTrue(request.user.has_perm(perm=None))
        self.admin.delete_model(request, self.user)
        self.assertFalse(User.objects.filter(pk=self.user.id).exists())
