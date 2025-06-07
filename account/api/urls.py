from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView
from account.views import UserProfileView
from .views import TagViewSet, TrackViewSet, TrackLogViewSet, MyTrackViewSet

router = DefaultRouter()
router.register(r"tracks", TrackViewSet, basename="track")
router.register(r"track-logs", TrackLogViewSet, basename="track-log")

tag_list = TagViewSet.as_view({"get": "list", "post": "create"})
my_track_view = MyTrackViewSet.as_view({"get": "list"})

urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("tags/", tag_list, name="tag-list"),
    path("my-tracks/", my_track_view, name="my-tracks"),
]

# اضافه کردن مسیرهای مربوط به ویوست‌ها (router)
urlpatterns += router.urls
