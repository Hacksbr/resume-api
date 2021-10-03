from django.contrib import admin

from profiles.models import Profile, SocialLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__name', 'occupation', 'contact_email', 'phone', 'city', 'country')
    list_display_links = ('id', 'user__name', 'occupation', 'contact_email', 'phone', 'city', 'country')
    list_filter = ('occupation', 'city', 'country')
    search_fields = ('user__name', 'occupation', 'contact_email', 'city', 'country')

    def user__name(self, obj):
        if obj.user:
            return obj.user.get_full_name

        return 'None'

    user__name.short_description = 'User\'s Name'
    user__name.admin_order_field = 'user__name'


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('github', 'linkedin', 'twitter', 'website')
    list_display_links = ('github', 'linkedin', 'twitter', 'website')
    list_filter = ('github', 'linkedin', 'twitter', 'website')
    search_fields = ('github', 'linkedin', 'twitter', 'website')
