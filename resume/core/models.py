# Python imports
import uuid

# Pip imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class ModelBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
