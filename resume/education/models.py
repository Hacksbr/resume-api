# Pip imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal imports
from resume.core.models import ModelBase


class Education(ModelBase):
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    gpa = models.FloatField(default=0.0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    city = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    country = models.CharField(max_length=50)

    profile = models.ForeignKey(
        'profiles.Profile', verbose_name='Profile', related_name='education', on_delete=models.CASCADE
    )

    skills = models.ManyToManyField('skills.Skill', related_name='education', blank=True, through='EducationSkill')

    def __str__(self):
        return f'{self.degree} in {self.field_of_study} at {self.school_name}'

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Education')
        ordering = ['-end_date', '-start_date']


class EducationSkill(ModelBase):
    education = models.ForeignKey(
        'Education', verbose_name='Education', related_name='education_skills', on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        'skills.Skill', verbose_name='Skill', related_name='education_skills', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    def __str__(self):
        return f'{self.education} - {self.skill}'

    class Meta:
        verbose_name = _('Education Skill')
        verbose_name_plural = _('Education Skills')
        ordering = ['order']
