from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Project, Task
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProjectSerializer,
    TaskSerializer,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):

        project = get_object_or_404(
            Project,
            pk=pk,
            owner=request.user
        )

        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)

        project.members.add(user)

        return Response(
            {
                "message": "Member added successfully.",
                "project": ProjectSerializer(project).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def change_owner(self, request, pk=None):

        project = get_object_or_404(
            Project,
            pk=pk,
            owner=request.user
        )

        owner = get_object_or_404(
            User,
            pk=request.data.get("owner")
        )

        project.owner = owner
        project.save()

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_200_OK
        )


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project__owner=self.request.user
        )

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):

        task = get_object_or_404(Task, pk=pk)

        user = get_object_or_404(
            User,
            pk=request.data.get("user_id")
        )

        task.assigned_to = user
        task.save()

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):

        task = get_object_or_404(Task, pk=pk)

        actual_hours = request.data.get("actual_hours")

        if actual_hours is not None:
            task.actual_hours = actual_hours

        task.status = "completed"
        task.save()

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )