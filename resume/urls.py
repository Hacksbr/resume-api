from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from resume.profiles.viewsets import ProfileViewSet
from resume.roles.viewsets import RoleViewSet
from resume.users.viewsets import UserViewSet

router = routers.DefaultRouter()
router.register('signup', UserViewSet)
router.register('profile', ProfileViewSet)
router.register('roles', RoleViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('resume-auth/', include('rest_framework.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Resume Administration'
admin.site.site_title = 'Resume Admin'
admin.site.index_title = 'Resume Admin'
