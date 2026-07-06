from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Student, Course, Enrollment
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    EnrollmentSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        student = self.get_object()

        courses = Course.objects.filter(
            enrollments__student=student
        )

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]