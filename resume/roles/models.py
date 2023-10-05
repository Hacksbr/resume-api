# Pip imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.core.models import ModelBase


class Role(ModelBase):
    class EmploymentTypes(models.TextChoices):
        FULL_TIME = 'full_time', _('Full-time')
        PART_TIME = 'part_time', _('Part-time')
        SELF_EMPLOYED = 'self_employed', _('Self-employed')
        FREELANCE = 'freelance', _('Freelance')
        CONTRACT = 'contract', _('Contract')
        INTERNSHIP = 'internship', _('Internship')
        APPRENTICESHIP = 'apprenticeship', _('Apprenticeship')
        LEADERSHIP_PROGRAM = 'leadership_program', _('Leadership Program')
        INDIRECT_CONTRACT = 'indirect_contract', _('Indirect Contract')
        VOLUNTEER = 'volunteer', _('Volunteer')
        OTHER = 'other', _('Other')

    company = models.CharField(_('Company'), max_length=50)
    title = models.CharField(_('Title'), max_length=50)
    employment_type = models.CharField(
        _('Employment Type'), max_length=50, choices=EmploymentTypes.choices, blank=True, null=True
    )
    about = models.CharField(_('About'), max_length=125, blank=True, null=True)

    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    city = models.CharField(_('City'), max_length=50)
    uf = models.CharField(_('UF'), max_length=2)
    country = models.CharField(_('Country'), max_length=50)

    is_current = models.BooleanField(_('Is Current'), default=False)
    is_active = models.BooleanField(_('Is Active'), default=True)

    profile = models.ForeignKey(
        'profiles.Profile', verbose_name=_('Profile'), related_name='roles', on_delete=models.CASCADE
    )

    skills = models.ManyToManyField(
        'skills.Skill', verbose_name=_('Skills'), related_name='role', blank=True, through='RoleSkill'
    )

    def __str__(self):
        return f'{self.title} at {self.company}'

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['-end_date', '-start_date']


class Achievement(ModelBase):
    description = models.CharField(_('Description'), max_length=125)
    order = models.PositiveIntegerField(_('Order'), default=0, blank=False, null=False, db_index=True)

    role = models.ForeignKey('Role', verbose_name=_('Role'), related_name='achievements', on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Achievement')
        verbose_name_plural = _('Achievements')
        ordering = ['order']


class RoleSkill(ModelBase):
    role = models.ForeignKey('Role', verbose_name=_('Role'), related_name='role_skills', on_delete=models.CASCADE)
    skill = models.ForeignKey(
        'skills.Skill', verbose_name=_('Skill'), related_name='role_skills', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(_('Order'), default=0, blank=False, null=False, db_index=True)

    def __str__(self):
        return f'{self.role} - {self.skill}'

    class Meta:
        verbose_name = _('Role Skill')
        verbose_name_plural = _('Role Skills')
        ordering = ['order']
