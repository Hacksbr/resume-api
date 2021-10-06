from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.response import Response

from profiles.models import Profile
from profiles.serializers import ProfileSerializer, ProfileCreateSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'uuid'
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance_serializer = ProfileSerializer(instance)
        return Response(instance_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_serializer_class(self):
        if self.action in ['create']:
            return ProfileCreateSerializer

        return ProfileSerializer
