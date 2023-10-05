# Pip imports
from rest_framework import viewsets

# Internal imports
from resume.education.models import Education
from resume.education.serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = []
