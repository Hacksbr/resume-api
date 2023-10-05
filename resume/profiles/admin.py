# Pip imports
from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField, SelectMultiple

# Internal imports
from resume.education.models import Education
from resume.profiles.models import Profile, SocialLink
from resume.roles.models import Role
from resume.skills.models import Skill


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class ProfileSkillInline(SortableStackedInline, admin.TabularInline):
    model = Profile.skills.through
    extra = 1


class ProfileAdminForm(ModelForm):
    skills = ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=SelectMultiple(attrs={'size': 10}),
    )

    class Meta:
        model = Profile
        fields = '__all__'


@admin.register(Profile)
class ProfileAdmin(SortableAdminBase, admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('id', 'user__name', 'occupation', 'contact_email', 'phone', 'profile__location', 'created_at')
    list_display_links = ('id', 'user__name', 'occupation', 'contact_email', 'phone')
    list_filter = ('occupation', 'city', 'country', 'created_at', 'updated_at')
    search_fields = ('user__name', 'occupation', 'contact_email', 'city', 'country')
    inlines = (
        SocialLinkInline,
        RoleInline,
        EducationInline,
        ProfileSkillInline,
    )

    def user__name(self, obj):
        if obj.user:
            return obj.user.get_full_name

        return 'None'

    user__name.short_description = 'User\'s Name'
    user__name.admin_order_field = 'user__name'

    def profile__location(self, obj):
        return obj.get_location

    profile__location.short_description = 'Location'
    profile__location.admin_order_field = 'profile__location'


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'is_active', 'profile__user__name')
    list_display_links = ('id', 'name', 'link', 'is_active', 'profile__user__name')
    list_filter = ('name', 'link', 'is_active')
    search_fields = ('name', 'link', 'is_active', 'profile__user__name')

    def profile__user__name(self, obj):
        if obj.profile.user:
            return obj.profile.user.get_full_name

        return 'None'

    profile__user__name.short_description = 'User\'s Name'
    profile__user__name.admin_order_field = 'profile__user__name'
