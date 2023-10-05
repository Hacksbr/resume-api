# Pip imports
from rest_framework import viewsets

# Internal imports
from resume.education.models import Education, Language
from resume.education.serializers import EducationSerializer, LanguageSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = []


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = []
