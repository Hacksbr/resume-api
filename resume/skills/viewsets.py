# Pip imports
from rest_framework import viewsets

# Internal imports
from resume.skills.models import Skill
from resume.skills.serializers import SkillSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = []
