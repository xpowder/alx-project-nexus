from django.urls import path
from .views import RegisterAPIView, UserProfileView

urlpatterns = [
    path("signup/", RegisterAPIView.as_view(), name="api_signup"),  
    path("me/", UserProfileView.as_view(), name="api_user_profile"),
]
