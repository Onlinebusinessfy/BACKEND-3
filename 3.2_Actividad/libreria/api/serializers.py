from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        if User.objects.count() == 1:

            group, created = Group.objects.get_or_create(name="ADMIN")

        else:

            group, created = Group.objects.get_or_create(name="CLIENT")

        user.groups.add(group)

        return user


class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "role"]

    def get_role(self, obj):

        grupo = obj.groups.first()

        if grupo:
            return grupo.name

        return None