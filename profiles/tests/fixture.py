import factory
from profiles.models import Profile, SocialLink


class SocialLinkFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SocialLink

    github = factory.Faker('url')
    linkedin = factory.Faker('url')
    twitter = factory.Faker('url')
    website = factory.Faker('url')


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory('users.tests.fixture.UserFactory')
    occupation = factory.Faker('job')
    contact_email = factory.Faker('company_email')
    phone = '+5516900000000'
    city = factory.Faker('city')
    country = factory.Faker('country')
    social_link = factory.SubFactory('profiles.tests.fixture.SocialLinkFactory')
