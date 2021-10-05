from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserSerializer
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

    def get_name(self, obj):  # noqa
        return str(obj)

    def get_location(self, obj):  # noqa
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


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    social_link = SocialLinkSerializer()

    class Meta:
        model = Profile
        lookup_field = 'uuid'
        fields = (
            'user',
            'occupation',
            'contact_email',
            'phone',
            'city',
            'country',
            'social_link',
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        social_link_data = validated_data.pop('social_link')

        user = User.objects.create_user(**user_data)
        social_link = SocialLink.objects.create(**social_link_data)

        profile = Profile.objects.create(user=user, social_link=social_link, **validated_data)
        return profile
