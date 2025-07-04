from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return HttpResponse("صفحه‌ی اصلی کار می‌کند!")



urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("api/account/", include("account.api.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)