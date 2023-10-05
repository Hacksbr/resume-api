# Pip imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.core.models import ModelBase


class Skill(ModelBase):
    name = models.CharField(_('Name'), max_length=50)
    category = models.CharField(_('Category'), max_length=50)
    type = models.CharField(_('Type'), max_length=50)
    language = models.CharField(_('Language'), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'language')
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ('name',)
