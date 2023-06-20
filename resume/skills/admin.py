# Pip imports
from django.contrib import admin

# Internal imports
from resume.skills.models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'type', 'language')
    list_display_links = ('name', 'category', 'type', 'language')
    list_filter = ('name', 'category', 'type', 'language')
    search_fields = ('name', 'category', 'type', 'language')
    ordering = ('name',)
