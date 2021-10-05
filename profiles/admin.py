from django.contrib import admin

from profiles.models import Profile, SocialLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__name', 'occupation', 'contact_email', 'phone', 'profile__location', 'created_at')
    list_display_links = ('id', 'user__name', 'occupation', 'contact_email', 'phone')
    list_filter = ('occupation', 'city', 'country', 'created_at', 'updated_at')
    search_fields = ('user__name', 'occupation', 'contact_email', 'city', 'country')

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
    list_display = ('id', 'github', 'linkedin', 'twitter', 'website')
    list_display_links = ('id', 'github', 'linkedin', 'twitter', 'website')
    list_filter = ('github', 'linkedin', 'twitter', 'website')
    search_fields = ('github', 'linkedin', 'twitter', 'website')
