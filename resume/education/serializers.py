# Pip imports
from rest_framework import serializers

# Internal imports
from resume.education.models import Education


class EducationSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Education
        fields = (
            'school_name',
            'degree',
            'field_of_study',
            'start_date',
            'end_date',
            'gpa',
            'description',
            'city',
            'uf',
            'country',
            'skills',
        )
