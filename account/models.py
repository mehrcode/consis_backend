from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
    Permission,
)


class CustomUserManager(UserManager):
    def _create_user(
        self, email, password=None, **extra_fields
    ):  # to create a private template for user creation
        if not email:
            raise ValueError("You have not specified a valid email")
        email = self.normalize_email(email)  # to get input email normalized
        user = self.model(
            email=email, **extra_fields
        )  # to specified the user authentication only with email
        user.set_password(password)  # to get password hashed
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=11, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    interests = models.ManyToManyField("Tag", blank=True)

    user_permissions = models.ManyToManyField(
        Permission, related_name="account_user_permissions", blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tracks"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TrackLog(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    progress_note = models.TextField(blank=True)
    minutes = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("track", "date")
        ordering = ['-date']
