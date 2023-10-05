# Pip imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.core.models import ModelBase


class Education(ModelBase):
    school_name = models.CharField(_('School Name'), max_length=255)
    degree = models.CharField(_('Degree'), max_length=255)
    field_of_study = models.CharField(_('Field of Study'), max_length=255)

    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    gpa = models.FloatField(_('GPA'), default=0.0, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    city = models.CharField(_('City'), max_length=50)
    uf = models.CharField(_('UF'), max_length=2)
    country = models.CharField(_('Country'), max_length=50)

    profile = models.ForeignKey(
        'profiles.Profile', verbose_name=_('Profile'), related_name='education', on_delete=models.CASCADE
    )

    skills = models.ManyToManyField(
        'skills.Skill', verbose_name=_('Skills'), related_name='education', blank=True, through='EducationSkill'
    )

    def __str__(self):
        return f'{self.degree} in {self.field_of_study} at {self.school_name}'

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Education')
        ordering = ['-end_date', '-start_date']


class EducationSkill(ModelBase):
    education = models.ForeignKey(
        'Education', verbose_name=_('Education'), related_name='education_skills', on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        'skills.Skill', verbose_name=_('Skill'), related_name='education_skills', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(_('Order'), default=0, blank=False, null=False, db_index=True)

    def __str__(self):
        return f'{self.education} - {self.skill}'

    class Meta:
        verbose_name = _('Education Skill')
        verbose_name_plural = _('Education Skills')
        ordering = ['order']


class Language(ModelBase):
    class LanguageLevels(models.TextChoices):
        BASIC = ('basic', _('Elementary proficiency'))
        INTERMEDIATE = ('intermediate', _('Limited working proficiency'))
        ADVANCED = ('advanced', _('Professional working proficiency'))
        FLUENT = ('fluent', _('Full professional proficiency'))
        NATIVE = ('native', _('Native or bilingual proficiency'))

    name = models.CharField(_('Name'), max_length=255, blank=False, null=False)
    level = models.CharField(_('Level'), max_length=12, choices=LanguageLevels.choices, blank=False, null=False)

    profile = models.ForeignKey(
        'profiles.Profile', verbose_name=_('Profile'), related_name='languages', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} - {self.level}'

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['name']
