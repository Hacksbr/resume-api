# Pip imports
from django.shortcuts import get_object_or_404
from rest_framework import permissions

# Internal imports
from resume.profiles.models import Profile


class IsUserProfileOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        profile = get_object_or_404(Profile, pk=view.kwargs.get('id'))

        if request.user.is_authenticated:
            if request.user == profile.user:
                return True

            if request.user.is_superuser:
                return True

        return False
