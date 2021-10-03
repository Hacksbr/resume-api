from django.contrib.auth import get_user_model
from rest_framework import serializers

from profiles.models import Profile, SocialLink

User = get_user_model()


class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialLink
        fields = (
            'github',
            'linkedin',
            'twitter',
            'website',
        )


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    social_link = SocialLinkSerializer()

    def get_name(self, obj):
        return str(obj)

    def get_location(self, obj):
        return obj.get_location

    class Meta:
        model = Profile
        lookup_field = 'uuid'
        fields = (
            'uuid',
            'name',
            'occupation',
            'contact_email',
            'location',
            'phone',
            'social_link',
        )
        read_only_fields = ('uuid',)
