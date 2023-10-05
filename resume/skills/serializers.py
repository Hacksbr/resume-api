# Pip imports
from rest_framework import serializers

# Internal imports
from resume.skills.models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            'name',
            'category',
            'type',
            'language',
        )
