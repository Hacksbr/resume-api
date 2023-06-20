# Pip imports
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.core.models import ModelBase


SOCIAL_NETWORKS = (
    ('GITHUB', _('GitHub')),
    ('LINKEDIN', _('LinkedIn')),
    ('TWITTER', _('Twitter')),
    ('WEBSITE', _('Website')),
    ('OTHER', _('Other')),
)


class Profile(ModelBase):
    user = models.OneToOneField('users.User', verbose_name='User', related_name='profile', on_delete=models.CASCADE)

    occupation = models.CharField(_('Occupation'), max_length=100, blank=False, null=False)
    contact_email = models.EmailField(_('Contact Email'), max_length=255, blank=True, null=True)
    phone = models.CharField(
        _('Phone'),
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+9999999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    city = models.CharField(_('City'), max_length=100, blank=False, null=False)
    country = models.CharField(_('Country'), max_length=80, blank=False, null=False)
    about = models.CharField(_('About'), max_length=550, blank=True, null=True)

    skills = models.ManyToManyField('skills.Skill', related_name='profile', blank=True, through='ProfileSkill')

    def __str__(self):
        return f'{self.user.get_full_name}'

    @property
    def get_location(self):
        return f'{self.city}, {self.country}'

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class SocialLink(ModelBase):
    class SocialNetworks(models.TextChoices):
        GITHUB = 'github', _('GitHub')
        LINKEDIN = 'linkedin', _('LinkedIn')
        TWITTER = 'twitter', _('Twitter')
        WEBSITE = 'website', _('Website')
        OTHER = 'other', _('Other')

    profile = models.ForeignKey(
        'Profile', verbose_name='Profile', related_name='social_links', on_delete=models.CASCADE
    )

    name = models.CharField(_('Name'), max_length=8, choices=SocialNetworks.choices, blank=False, null=False)
    link = models.CharField(_('Link'), max_length=255, blank=False, null=False)
    is_active = models.BooleanField(_('Active'), default=True)

    def __str__(self):
        return self.name

    @property
    def get_username(self):
        return self.link.rstrip('/').split('/')[-1] if self.name not in ['website', 'other'] else ''

    class Meta:
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')


class ProfileSkill(ModelBase):
    profile = models.ForeignKey(
        'Profile', verbose_name='Profile', related_name='profile_skills', on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        'skills.Skill', verbose_name='Skill', related_name='profile_skills', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    def __str__(self):
        return f'{self.profile} - {self.skill}'

    class Meta:
        verbose_name = _('Profile Skill')
        verbose_name_plural = _('Profile Skills')
        ordering = ['order']
