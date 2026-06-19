from django.db.models import Avg, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Student, Course, Enrollment
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    EnrollmentSerializer
)


class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):

        queryset = Student.objects.all()

        name = self.request.query_params.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):

        student = self.get_object()

        courses = Course.objects.filter(
            enrollments__student=student
        )

        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def average_above_90(self, request):

        students = Student.objects.annotate(
            avg_grade=Avg('enrollments__final_grade')
        ).filter(avg_grade__gt=90)

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):

        course = self.get_object()

        students = Student.objects.filter(
            enrollments__course=course
        )

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def more_than_5_students(self, request):

        courses = Course.objects.annotate(
            total_students=Count('enrollments')
        ).filter(total_students__gt=5)

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer