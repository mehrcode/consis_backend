from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView
from account.views import UserProfileView
from .views import TagViewSet


tag_list = TagViewSet.as_view({"get": "list", "post": "create"})

urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("tags/", tag_list, name="tag-list"),
]
