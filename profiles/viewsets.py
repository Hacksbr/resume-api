from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets

from profiles.models import Profile
from profiles.serializers import ProfileSerializer

User = get_user_model()


class ProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'uuid'
    permission_classes = []
