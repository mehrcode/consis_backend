from rest_framework import serializers
from .models import User


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
