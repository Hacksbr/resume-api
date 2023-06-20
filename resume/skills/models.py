# Pip imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.core.models import ModelBase


class Skill(ModelBase):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'language')
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ('name',)
