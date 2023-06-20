# Pip imports
from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin

# Internal imports
from resume.roles.models import Achievement, Role


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('role__company', 'role__title', 'description', 'order')
    list_display_links = ('description', 'order', 'role__title', 'role__company')
    list_filter = ('description', 'order', 'role__title', 'role__company')
    search_fields = ('description', 'order', 'role')
    readonly_fields = ('created_at', 'updated_at')
    ordering = (
        '-role__end_date',
        '-role__start_date',
        'order',
    )

    def role__title(self, obj):
        if obj.role:
            return obj.role.title

        return 'None'

    role__title.short_description = 'Role Title'
    role__title.admin_order_field = 'role__title'

    def role__company(self, obj):
        if obj.role:
            return obj.role.company

        return 'None'

    role__company.short_description = 'Role Company'
    role__company.admin_order_field = 'role__company'


class AchievementInline(SortableStackedInline, admin.TabularInline):
    model = Achievement
    extra = 1


@admin.register(Role)
class RoleAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('company', 'title', 'employment_type', 'start_date', 'end_date', 'is_current', 'is_active')
    list_display_links = ('title', 'company', 'employment_type', 'start_date', 'end_date', 'is_current', 'is_active')
    list_filter = ('company', 'title', 'about', 'country', 'skills__name')
    search_fields = ('company', 'title', 'about', 'country', 'achievements__description', 'skills__name')
    ordering = ('-end_date', '-start_date')
    readonly_fields = ('skills', 'created_at', 'updated_at')
    inlines = [AchievementInline]
