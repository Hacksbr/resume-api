from django.conf.urls import url
from .views import UserRegistrationView
from .views import UserLoginView

urlpatterns = [
    url('/api/v1/register/', UserRegistrationView.as_view()),
    url('/api/v1/login/', UserLoginView.as_view()),
    ]