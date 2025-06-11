from django.urls import path, include
from . import views


urlpatterns = [
    # path("api/", include("account.api.urls")), 
    path("api/account/", include("account.api.urls")), #just for test
    path("register/", views.RegisterView.as_view(), name="register"),
]
