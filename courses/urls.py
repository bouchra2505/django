from django.urls import path
from .views import (
    CourseListCreateView,
    CourseDetailView,
    SearchCourseView,
    CourseByScheduleView,
    EnrollStudentView,
    CoursesByStudentView,
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/search/', SearchCourseView.as_view(), name='course-search'),
    path('courses/schedule/', CourseByScheduleView.as_view(), name='course-schedule'),
    path('courses/enroll/', EnrollStudentView.as_view(), name='course-enroll'),
    path('students/<int:student_id>/courses/', CoursesByStudentView.as_view(), name='student-courses'),
]
