# Pip imports
from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin

# Internal imports
from resume.education.models import Education, EducationSkill, Language


class EducationSkillInline(SortableStackedInline, admin.TabularInline):
    model = EducationSkill
    extra = 1


@admin.register(Education)
class EducationAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('school_name', 'degree', 'field_of_study', 'start_date', 'end_date')
    list_display_links = ('school_name', 'degree', 'field_of_study', 'start_date', 'end_date')
    list_filter = ('school_name', 'degree', 'field_of_study', 'start_date', 'end_date')
    search_fields = ('school_name', 'degree', 'field_of_study')
    ordering = ('-end_date', '-start_date')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [EducationSkillInline]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    list_display_links = ('name', 'level')
    list_filter = ('name', 'level')
    search_fields = ('name', 'level')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
