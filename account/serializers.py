from rest_framework import serializers
from .models import User
from account.api.serializers import TagSerializer
from .models import Tag, Track, TrackLog
from datetime import timedelta
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Ensures password isn't exposed in responses

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(
                validated_data["password"]
            )  # Hash the password on update
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    interests = TagSerializer(many=True, read_only=True)
    interest_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source="interests",
    )

    profile_image = serializers.ImageField(use_url=True)
    

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "bio",
            "location",
            "instagram_url",
            "website_url",
            "date_of_birth",
            "interests",
            "interest_ids",
            "profile_image",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


class TrackSerializer(serializers.ModelSerializer):
    last_log = serializers.SerializerMethodField()
    streak_days = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            "id",
            "name",
            "created_at",
            "unit",
            "goal",
            "last_log",
            "streak_days", 
        ]

    def get_last_log(self, obj):
        last_log = obj.logs.order_by("-date").first()
        if last_log:
            return TrackLogSerializer(last_log).data
        return None

    def get_streak_days(self, obj):
        today = timezone.localdate()
        logs = obj.logs.order_by("-date").values_list("date", flat=True)
        streak = 0
        current_day = today

        for log_date in logs:
            if log_date == current_day:
                streak += 1
                current_day -= timedelta(days=1)
            elif log_date == current_day - timedelta(days=1):
                current_day = log_date
                streak += 1
                current_day -= timedelta(days=1)
            else:
                break

        return streak


class TrackLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackLog
        fields = ["date", "minutes", "score", "progress_note"]
