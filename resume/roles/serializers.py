# Pip imports
from rest_framework import serializers

# Internal imports
from resume.roles.models import Achievement, Role


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = (
            'id',
            'description',
            'order',
        )


class RoleSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True)
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Role
        fields = (
            'company',
            'title',
            'employment_type',
            'about',
            'start_date',
            'end_date',
            'city',
            'uf',
            'country',
            'is_current',
            'is_active',
            'achievements',
            'skills',
        )
