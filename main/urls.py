from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("صفحه‌ی اصلی کار می‌کند!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("api/account/", include("account.api.urls")),
]
