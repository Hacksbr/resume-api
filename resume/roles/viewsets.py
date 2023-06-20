# Pip imports
from rest_framework import viewsets

# Internal imports
from resume.roles.models import Achievement, Role
from resume.roles.serializers import AchievementSerializer, RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = []


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = []
