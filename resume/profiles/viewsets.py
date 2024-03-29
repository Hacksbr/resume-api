# Pip imports
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Internal imports
from resume.profiles import serializers
from resume.profiles.models import Profile
from resume.profiles.permissions import IsUserProfileOrAdmin


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance_serializer = serializers.ProfileSerializer(instance)
        return Response(instance_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        if not request.data.get('user'):
            return Response(dict(error='Attribute \'user\' is missing.'), status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('social_links'):
            return Response(dict(error='Attribute \'social_link\' is missing.'), status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        self.perform_destroy(instance)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        instance = request.user.profile
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProfileCreateSerializer

        if self.action in ['update', 'partial_update']:
            return serializers.ProfileUpdateSerializer

        return serializers.ProfileSerializer

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (permissions.IsAuthenticated, IsUserProfileOrAdmin)

        if self.action in ['me']:
            self.permission_classes = (permissions.IsAuthenticated,)

        return super().get_permissions()
