# Python imports
import uuid

# Pip imports
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Change the default User Model beahavier to login with 'email'.
    """

    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_('email address'), max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting account'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_trusty = models.BooleanField(
        _('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.')
    )

    USERNAME_FIELD = 'email'  # Set email as a default login field
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'
