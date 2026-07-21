from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Project, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        exclude = ("internal_notes",)

    def validate_budget(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Budget cannot be negative."
            )
        return value


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ("confidential_comment",)

    def validate_estimated_hours(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Estimated hours cannot be negative."
            )
        return value

    def validate_actual_hours(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Actual hours cannot be negative."
            )
        return value