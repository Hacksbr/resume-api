import factory
from faker import Faker

from resume.profiles.models import Profile, SocialLink


def _get_link():
    fake = Faker(['pt_BR'])
    return f'{fake.url()}{fake.user_name()}'


class SocialLinkFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SocialLink

    profile = factory.SubFactory('resume.profiles.tests.fixture.ProfileFactory')
    name = factory.Faker('random_element', elements=('github', 'linkedin', 'twitter', 'website', 'other'))
    link = _get_link()


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory('resume.users.tests.fixture.UserFactory')
    occupation = factory.Faker('job')
    contact_email = factory.Faker('company_email')
    phone = '+5516900000000'
    city = factory.Faker('city')
    country = factory.Faker('country')
