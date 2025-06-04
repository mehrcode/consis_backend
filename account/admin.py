from django.contrib import admin

# Register your models here.
from django.contrib import admin
from account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    ]


admin.site.register(User, UserAdmin)
