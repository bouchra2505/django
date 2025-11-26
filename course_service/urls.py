from django.urls import path, include

from courses import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),  # changed from 'api/' to 'courses/'
]
