# Pip imports
from rest_framework import serializers

# Internal imports
from resume.profiles.models import Profile, SocialLink
from resume.roles.serializers import RoleSerializer
from resume.skills.serializers import SkillSerializer
from resume.users.models import User
from resume.users.serializers import UserSerializer, UserUpdateSerializer


def update_attr(instance, data, attributes):
    [setattr(instance, attr, data.get(attr, getattr(instance, attr))) for attr in attributes]


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = (
            'name',
            'link',
            'is_active',
        )


class SocialLinkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = (
            'id',
            'name',
            'link',
            'is_active',
        )
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True)
    roles = RoleSerializer(many=True)
    skills = SkillSerializer(many=True)

    def get_name(self, obj):  # noqa
        return str(obj)

    def get_location(self, obj):  # noqa
        return obj.get_location

    class Meta:
        model = Profile
        fields = (
            'name',
            'occupation',
            'contact_email',
            'location',
            'phone',
            'about',
            'social_links',
            'skills',
            'roles',
        )


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'occupation',
            'contact_email',
            'phone',
            'city',
            'country',
            'about',
            'social_links',
        )
        read_only_fields = ('social_links',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        social_link_data = validated_data.pop('social_links')

        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)

        SocialLink.objects.bulk_create([SocialLink(profile=profile, **item) for item in social_link_data])

        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    social_links = SocialLinkUpdateSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'occupation',
            'contact_email',
            'phone',
            'city',
            'country',
            'social_links',
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        social_links_data = validated_data.pop('social_links')

        user = instance.user

        attributes = ['occupation', 'contact_email', 'phone', 'city', 'country']
        update_attr(instance, validated_data, attributes)
        instance.save()

        attributes = ['first_name', 'last_name']
        update_attr(user, user_data, attributes)
        user.save()

        social_link_objs = []
        for item in social_links_data:
            social_link, created = SocialLink.objects.get_or_create(
                id=item.get('id'),
                profile_id=instance.id,
                defaults={'name': item.get('name'), 'link': item.get('link'), 'is_active': item.get('is_active')},
            )

            if not created:
                social_link.link = item.get('link')
                social_link.is_active = item.get('is_active')
                social_link_objs.append(social_link)

        SocialLink.objects.bulk_update(social_link_objs, ['link', 'is_active'])

        return instance
