import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, verbose_name='User',
        related_name='user_profile',
        on_delete=models.CASCADE
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    occupation = models.CharField('Occupation', max_length=100, blank=False, null=False)
    contact_email = models.EmailField('Contact Email', max_length=255, blank=True, null=True)
    phone = models.CharField(
        'Phone', max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+9999999999999'. Up to 15 digits allowed."
        )]
    )
    city = models.CharField('City', max_length=100, blank=False, null=False)
    country = models.CharField('Country', max_length=80, blank=False, null=False)

    social_link = models.OneToOneField(
        'SocialLink', verbose_name='Social Link ',
        related_name='%(app_label)s_%(class)s_profile',
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return f'{self.user.get_full_name}'

    @property
    def get_location(self):
        return f'{self.city}, {self.country}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class SocialLink(models.Model):
    github = models.CharField('GitHub', max_length=100, blank=True, null=True)
    linkedin = models.CharField('LinkedIn', max_length=100, blank=True, null=True)
    twitter = models.CharField('Twitter', max_length=100, blank=True, null=True)
    website = models.CharField('Website', max_length=100, blank=True, null=True)

    def __str__(self):
        if self.github:
            return self.get_github_user

        if self.linkedin:
            return self.get_linkedin_user

        if self.twitter:
            return self.get_twitter_user

        return self.website

    @property
    def get_github_user(self):
        return self.github.split('/')[-1]

    @property
    def get_linkedin_user(self):
        return self.linkedin.split('/')[-1]

    @property
    def get_twitter_user(self):
        return self.twitter.split('/')[-1]

    class Meta:
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
