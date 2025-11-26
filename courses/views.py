from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Course, StudentCourse
from .serializers import CourseSerializer, StudentCourseSerializer


# List & Create Courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Retrieve, Update, Delete a Single Course
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Search Courses by name, instructor, or category
class SearchCourseView(APIView):
    def get(self, request):
        name = request.GET.get('name')
        instructor = request.GET.get('instructor')
        category = request.GET.get('category')

        queryset = Course.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        if instructor:
            queryset = queryset.filter(instructor__icontains=instructor)
        if category:
            queryset = queryset.filter(category__icontains=category)

        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)
    

# Filter by schedule (day/time)
class CourseByScheduleView(APIView):
    def get(self, request):
        day = request.GET.get('day')
        time = request.GET.get('time')

        filtered_courses = []
        for course in Course.objects.all():
            schedule = course.schedule or {}
            if day in schedule:
                if not time or schedule[day] == time:
                    filtered_courses.append(course)

        serializer = CourseSerializer(filtered_courses, many=True)
        return Response(serializer.data)


# Enroll a student in a course
class EnrollStudentView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        course_id = request.data.get('course_id')

        try:
            course = Course.objects.get(id=course_id)
            StudentCourse.objects.create(student_id=student_id, course=course)
            return Response(
                {"message": f"Student {student_id} enrolled in {course.name}"},
                status=status.HTTP_201_CREATED
            )
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


# Get all courses for a student
class CoursesByStudentView(APIView):
    def get(self, request, student_id):
        enrollments = StudentCourse.objects.filter(student_id=student_id)
        course_ids = [e.course.id for e in enrollments]
        courses = Course.objects.filter(id__in=course_ids)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
